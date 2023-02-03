"""
@Project, that tracks and estimates real time posture for desk workers.

@Author: Emir Cetin Memis

@Contributors:
    - Ahmet Yildiz
    - Pelin Mise
    - Barkin Topcu
    - Cem Baysal

@Date: 2/2/2023
"""

from    Utilities   import safe_start, safe_stop
from    GUI         import Application

if __name__ == "__main__" :

    safe_start()

    Application().mainloop()

    safe_stop()