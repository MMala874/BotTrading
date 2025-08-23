from collections import OrderedDict

class PositionManager:
    """
    Coordina più bot sullo stesso simbolo, evitando conflitti nocivi.
    Policies:
    - block_opposite: blocca ordini opposti se presente long aperto su quel simbolo da un altro bot
    - netting: netta le posizioni (chiude long se arriva short opposto, rispettando priorità bot)
    - allow: nessun controllo (sconsigliato)
    """
    def __init__(self, policy: str = "block_opposite", bot_priority: list[str] | None = None, max_currency_exposure: dict[str,int] | None = None):
        self.policy = policy
        self.active = {}  # key: (symbol, bot) -> "LONG"/"SHORT"
        self.priority = bot_priority or []
        self.max_currency_exposure = max_currency_exposure or {}

    def _priority(self, bot_name: str) -> int:
    def _currencies(self, symbol: str) -> tuple[str,str]:
        # tenta parse EURUSD o EURUSD=X
        s = ''.join([c for c in symbol if c.isalpha()])  # rimuove '=' o altri
        base = s[:3].upper() if len(s)>=6 else s[:3].upper()
        quote = s[3:6].upper() if len(s)>=6 else s[3:6].upper()
        return base, quote

    def _currency_exposure_ok(self, symbol: str) -> bool:
        if not self.max_currency_exposure:
            return True
        base, quote = self._currencies(symbol)
        counts = {}
        for (sym, _bot), side in self.active.items():
            b,q = self._currencies(sym)
            counts[b] = counts.get(b,0) + 1
            counts[q] = counts.get(q,0) + 1
        for cur in (base, quote):
            limit = self.max_currency_exposure.get(cur)
            if limit is not None and counts.get(cur,0) >= limit:
                return False
        return True

        try: return self.priority.index(bot_name)
        except ValueError: return len(self.priority)

    def can_open(self, symbol: str, bot_name: str, side: str) -> bool:
        side = side.upper()
        # check existing positions on symbol
        existing = [(b, s) for (sym, b), s in self.active.items() if sym == symbol]
        if not self._currency_exposure_ok(symbol):
            return False
        if not existing: return True
        if self.policy == "allow": return True
        if self.policy == "block_opposite":
            # blocca se qualsiasi altro bot è nella direzione opposta
            return not any(((s == "LONG" and side=="SHORT") or (s=="SHORT" and side=="LONG")) for _, s in existing)
        if self.policy == "netting":
            # consenti solo se VINCI priorità (sostituisci posizione)
            best_bot, best_side = sorted(existing, key=lambda x: self._priority(x[0]))[0]
            return self._priority(bot_name) < self._priority(best_bot) or all(s==side for _, s in existing)
        return True

    def register_open(self, symbol: str, bot_name: str, side: str):
        self.active[(symbol, bot_name)] = "LONG" if side.upper()=="BUY" else "SHORT"

    def register_close(self, symbol: str, bot_name: str):
        self.active.pop((symbol, bot_name), None)
