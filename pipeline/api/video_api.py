"""Video generation API — provider abstraction with Kling/fal.ai implementation.

Base class VideoProvider with swappable concrete providers.
Kling uses fal.ai as intermediary: submit → poll → download.
Future providers added as new subclasses.
"""

from abc import ABC, abstractmethod
from pathlib import Path


class VideoProvider(ABC):
    """Abstract base for video generation providers."""

    @abstractmethod
    def generate(self, image_path: Path, prompt: str, output_path: Path) -> Path:
        """Generate a video from a source image and motion prompt.

        Args:
            image_path: Path to the source image for image-to-video generation.
            prompt: Motion/animation prompt describing desired video movement.
            output_path: File path where the generated video should be saved.

        Returns:
            Path to the saved video file.
        """
        ...


class KlingProvider(VideoProvider):
    """Kling video generation via fal.ai.

    Image-to-video, 1920x1080, 10 seconds.
    Async pattern: submit job → poll for completion → download result.
    """

    def generate(self, image_path: Path, prompt: str, output_path: Path) -> Path:
        """Generate a video using Kling via fal.ai.

        Args:
            image_path: Source image for the video.
            prompt: Motion prompt for the video.
            output_path: Where to save the generated MP4.

        Returns:
            Path to the saved video.
        """
        pass


class PlaceholderVideoProvider(VideoProvider):
    """Dry-run provider — prints what would be generated without making API calls."""

    def generate(self, image_path: Path, prompt: str, output_path: Path) -> Path:
        """Print a dry-run message instead of generating a video.

        Args:
            image_path: Source image (logged but not used).
            prompt: Motion prompt (logged but not used).
            output_path: Where the video would be saved.

        Returns:
            The output_path (no file is actually created).
        """
        pass


def get_video_provider(provider_name: str = "kling", dry_run: bool = False) -> VideoProvider:
    """Factory function returning the appropriate VideoProvider instance.

    Args:
        provider_name: Provider key ('kling', 'runway', 'pika', 'luma').
        dry_run: If True, always returns PlaceholderVideoProvider.

    Returns:
        A VideoProvider instance ready to generate videos.
    """
    pass
