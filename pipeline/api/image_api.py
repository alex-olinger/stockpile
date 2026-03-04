"""Image generation API — provider abstraction with Gemini and placeholder implementations.

Base class ImageProvider with swappable concrete providers.
Future providers (DALL-E, Flux, Ideogram) added as new subclasses.
"""

from abc import ABC, abstractmethod
from pathlib import Path


class ImageProvider(ABC):
    """Abstract base for image generation providers."""

    @abstractmethod
    def generate(self, prompt: str, output_path: Path) -> Path:
        """Generate an image from a text prompt and save it.

        Args:
            prompt: Text description of the image to generate.
            output_path: File path where the generated image should be saved.

        Returns:
            Path to the saved image file.
        """
        ...


class GeminiProvider(ImageProvider):
    """Google Gemini image generation via the google-genai SDK.

    Generates 1920x1080 photorealistic images.
    """

    def generate(self, prompt: str, output_path: Path) -> Path:
        """Generate an image using Google Gemini API.

        Args:
            prompt: Text description of the image.
            output_path: Where to save the generated PNG.

        Returns:
            Path to the saved image.
        """
        from google import genai
        from pipeline.config import GOOGLE_API_KEY

        client = genai.Client(api_key=GOOGLE_API_KEY)
        response = client.models.generate_images(
            model="imagen-3.0-generate-002",
            prompt=prompt,
            config=genai.types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="16:9",
            ),
        )
        image_bytes = response.generated_images[0].image.image_bytes
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(image_bytes)
        return output_path


class PlaceholderProvider(ImageProvider):
    """Dry-run provider — creates 1920x1080 solid-color PNGs with prompt text overlay.

    Uses Pillow to create placeholder images without any API calls.
    """

    def generate(self, prompt: str, output_path: Path) -> Path:
        """Create a placeholder image with the prompt text overlaid.

        Args:
            prompt: Text to display on the placeholder image.
            output_path: Where to save the placeholder PNG.

        Returns:
            Path to the saved placeholder image.
        """
        from PIL import Image, ImageDraw

        img = Image.new("RGB", (1920, 1080), color=(70, 130, 180))
        draw = ImageDraw.Draw(img)
        # Wrap long prompts to fit
        max_chars = 60
        lines = [prompt[i:i + max_chars] for i in range(0, len(prompt), max_chars)]
        text = "\n".join(lines[:10])
        draw.text((40, 40), f"[PLACEHOLDER]\n\n{text}", fill=(255, 255, 255))
        output_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(output_path, "PNG")
        return output_path


def get_image_provider(provider_name: str = "gemini", dry_run: bool = False) -> ImageProvider:
    """Factory function returning the appropriate ImageProvider instance.

    Args:
        provider_name: Provider key ('gemini', 'dall-e', 'flux', 'ideogram').
        dry_run: If True, always returns PlaceholderProvider.

    Returns:
        An ImageProvider instance ready to generate images.
    """
    if dry_run:
        return PlaceholderProvider()
    if provider_name == "gemini":
        return GeminiProvider()
    raise ValueError(f"Unknown image provider: {provider_name}")
