"""
Genre schema for domain model
"""

from enum import StrEnum

from app.exceptions.base_exceptions_schema import SpotifyElectronException
from app.logging.logging_constants import LOGGING_GENRE_CLASS
from app.logging.logging_schema import SpotifyElectronLogger

genre_class_logger = SpotifyElectronLogger(LOGGING_GENRE_CLASS).getLogger()


class Genre(StrEnum):
    """Song genres"""

    POP = "Pop"
    ROCK = "Rock"
    HIP_HOP = "Hip-hop"
    RNB = "R&B (Rhythm and Blues)"
    JAZZ = "Jazz"
    BLUES = "Blues"
    REGGAE = "Reggae"
    COUNTRY = "Country"
    FOLK = "Folk"
    CLASSICAL = "Classical"
    ELECTRONICA = "Electronic"
    DANCE = "Dance"
    METAL = "Metal"
    PUNK = "Punk"
    FUNK = "Funk"
    SOUL = "Soul"
    GOSPEL = "Gospel"
    LATIN = "Latin"
    WORLD_MUSIC = "World Music"
    EXPERIMENTAL = "Experimental"
    AMBIENT = "Ambient"
    FUSION = "Fusion"
    INSTRUMENTAL = "Instrumental"
    ALTERNATIVE = "Alternative"
    INDIE = "Indie"
    RAP = "Rap"
    SKA = "Ska"
    GRUNGE = "Grunge"
    TRAP = "Trap"
    REGGAETON = "Reggaeton"
    ACOUSTIC = "Acoustic"
    DISCO = "Disco"
    HARDSTYLE = "Hardstyle"
    OPERA = "Opera"
    PHONK = "Phonk"
    TECHNO = "Techno"

    @staticmethod
    def check_valid_genre(genre: str) -> bool:
        """Checks if the genre is valid and raises an exception if not"""
        if genre not in {member.value for member in Genre}:
            genre_class_logger.exception(f"Genre {genre} is not a valid Genre")
            raise GenreNotValidException
        return True

    @staticmethod
    def get_genre_string_value(genre: StrEnum) -> str:
        """Gets genre string representation value from Genre

        Args:
            genre (Enum): the genre Enum

        Raises:
            GenreNotValidException: if the genre doesn't match any existing genres

        Returns:
            str: the string representation of the genre
        """
        try:
            return str(genre.value)
        except Exception as exception:
            genre_class_logger.exception(f"Genre {genre} is not a valid Genre")
            raise GenreNotValidException from exception


class GenreNotValidException(SpotifyElectronException):
    """Exception for getting a Genre from an invalid value"""

    ERROR = "The genre doesnt exists"

    def __init__(self):
        super().__init__(self.ERROR)


class GenreServiceException(SpotifyElectronException):
    """Exception for unexpected error getting genres"""

    ERROR = "Unexpected error while getting genres"

    def __init__(self):
        super().__init__(self.ERROR)
