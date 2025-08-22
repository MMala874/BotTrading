
from datetime import datetime
import dukascopy_python
from dukascopy_python.instruments import INSTRUMENT_FX_MAJORS_EUR_USD
from dukascopy_python import OFFER_SIDE_BID, INTERVAL_HOUR_1

def get_data_dukascopy(symbol=INSTRUMENT_FX_MAJORS_EUR_USD,
                       start="2015-01-01",
                       end=None,
                       interval=INTERVAL_HOUR_1,
                       offer_side=OFFER_SIDE_BID):
    """
    Scarica dati storici da Dukascopy. Restituisce un pd.DataFrame.
    """
    df = dukascopy_python.fetch(
        instrument=symbol,
        interval=interval,
        offer_side=offer_side,
        start=datetime.fromisoformat(start),
        end=datetime.fromisoformat(end) if end else None
    )
    return df
