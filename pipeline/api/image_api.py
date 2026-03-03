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
        pass


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
        pass


def get_image_provider(provider_name: str = "gemini", dry_run: bool = False) -> ImageProvider:
    """Factory function returning the appropriate ImageProvider instance.

    Args:
        provider_name: Provider key ('gemini', 'dall-e', 'flux', 'ideogram').
        dry_run: If True, always returns PlaceholderProvider.

    Returns:
        An ImageProvider instance ready to generate images.
    """
    pass
