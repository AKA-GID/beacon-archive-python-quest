"""Private-at-runtime catalogue for the "Beacon Archive" string quest.

The catalogue contains generators, not fixed answers.  ``build_catalog`` is
called once when the service starts; only generated inputs are returned by the
public API, while the expected JSON stays in the server process.
"""
from __future__ import annotations

import random


RNG = random.SystemRandom()


def _choice(values):
    return RNG.choice(values)


def _symbol():
    word = _choice(["маяк", "орбита", "сигнал", "комета", "радар"])
    index = RNG.randrange(len(word))
    return {"word": word, "index": index}, {"symbol": word[index]}


def _ribbon():
    message = _choice(["северныймаяк", "лунныйпередатчик", "тихийсигнал"])
    start = RNG.randrange(0, len(message) - 2)
    end = RNG.randrange(start + 2, len(message) + 1)
    return {"message": message, "start": start, "end": end}, {"fragment": message[start:end]}


def _mirror():
    word = _choice(["маяк", "вектор", "спутник", "контур"])
    return {"word": word}, {"reflection": word[::-1]}


def _clean_call():
    phrase = _choice(["  СЕВЕР-7  ", "\tОрбита-3 ", "  ТИХИЙ МАЯК\n"])
    return {"phrase": phrase}, {"clean": phrase.strip().lower()}


def _beacon_label():
    callsign = _choice(["тихий маяк", "лунный порт", "северный луч"])
    return {"callsign": callsign}, {"label": callsign.title().replace(" ", "-")}


def _echo_count():
    signal = _choice(["МаЯк-маяк-МаяК", "сИГнал сигнал СИГНАЛ", "радар РАДАР раДар"])
    symbol = _choice(sorted(set(signal.lower()) - {" ", "-"}))
    return {"signal": signal, "symbol": symbol}, {"count": signal.lower().count(symbol)}


def _signal_window():
    message, marker = _choice([
        ("курс:север;маяк:готов", "маяк"),
        ("канал-7|приём|ответ", "приём"),
        ("орбита/связь/стабильна", "связь"),
    ])
    return {"message": message, "marker": marker}, {"position": message.find(marker)}


def _call_sign():
    name = _choice(["north", "luna", "vector", "delta"])
    sector = RNG.randint(1, 99)
    return {"name": name, "sector": sector}, {"callsign": f"{name.upper()}-{sector:02d}"}


def _channel_code():
    word = _choice(["передатчик", "координата", "радиограмма"])
    step = _choice([2, 3])
    return {"word": word, "step": step}, {"code": word[::step]}


def _dispatch():
    callsign = _choice(["NORTH-07", "LUNA-12", "VECTOR-04"])
    sector = RNG.randint(1, 9)
    channel = RNG.randint(10, 99)
    priority = _choice(["high", "normal", "low"])
    packet = f"TO:{callsign} | sector={sector:02d} | channel={channel} | priority={priority.upper()}"
    return (
        {"callsign": callsign, "sector": sector, "channel": channel, "priority": priority},
        {"packet": packet},
    )


def _final_transmission():
    message = _choice(["радиомаякготов", "связьвосстановлена", "орбитачистая"])
    start = RNG.randrange(0, len(message) - 3)
    length = RNG.randint(3, min(6, len(message) - start))
    fragment = message[start:start + length].upper()
    return (
        {"message": message, "start": start, "length": length},
        {"transmission": f"{fragment}:{len(message)}"},
    )


TASK_BUILDERS = {
    "1.1": _symbol,
    "1.2": _ribbon,
    "1.3": _mirror,
    "2.1": _clean_call,
    "2.2": _beacon_label,
    "2.3": _echo_count,
    "3.1": _signal_window,
    "3.2": _call_sign,
    "3.3": _channel_code,
    "4.1": _dispatch,
    "4.2": _final_transmission,
}


def build_catalog():
    """Return a fresh, ordered ``task_id -> {input, expected}`` mapping."""
    return {
        task_id: {"input": values[0], "expected": values[1]}
        for task_id, builder in TASK_BUILDERS.items()
        for values in [builder()]
    }
