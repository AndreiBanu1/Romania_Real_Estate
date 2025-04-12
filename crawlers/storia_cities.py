from enum import Enum

class StoriaCity(Enum):
    TOATA_ROMANIA = "toata-romania"
    ALBA = "alba"
    ARAD = "arad"
    ARGES = "arges"
    BACAU = "bacau"
    BIHOR = "bihor"
    BISTRITA_NASAUD = "bistrita--nasaud"
    BOTOSANI = "botosani"
    BRAILA = "braila"
    BRASOV = "brasov"
    BUCURESTI = "bucuresti"
    BUZAU = "buzau"
    CALARASI = "calarasi"
    CARAS_SEVERIN = "caras--severin"
    CLUJ = "cluj"
    CONSTANTA = "constanta"
    COVASNA = "covasna"
    DAMBOVITA = "dambovita"
    DOLJ = "dolj"
    GALATI = "galati"
    GIURGIU = "giurgiu"
    GORJ = "gorj"
    HARGHITA = "harghita"
    HUNEDOARA = "hunedoara"
    IALOMITA = "ialomita"
    IASI = "iasi"
    ILFOV = "ilfov"
    MARAMURES = "maramures"
    MEHEDINTI = "mehedinti"
    MURES = "mures"
    NEAMT = "neamt"
    OLT = "olt"
    PRAHOVA = "prahova"
    SALAJ = "salaj"
    SATU_MARE = "satu-mare"
    SIBIU = "sibiu"
    SUCEAVA = "suceava"
    TELEORMAN = "teleorman"
    TIMIS = "timis"
    TULCEA = "tulcea"
    VALCEA = "valcea"
    VASLUI = "vaslui"
    VRANCEA = "vrancea"

    @staticmethod
    def get_city_slug(city_name: str):
        """Converts a given city name to its corresponding slug."""
        city_name = city_name.lower().replace(" ", "_").replace("-", "_")
        return getattr(StoriaCity, city_name.upper(), None)
