# -*- coding: utf-8 -*-
import numpy as np


def events_to_mne(events, event_conditions=None):
    """**Create MNE-compatible events**

    Create `MNE <https://mne.tools/stable/index.html>`_ compatible events for integration with M/
    EEG.

    Parameters
    ----------
    events : list or ndarray or dict
        Events onset location. Can also be a dict obtained through :func:`.events_find'.
    event_conditions : list
        An optional list containing, for each event, for example the trial category, group or
        experimental conditions. Defaults to ``None``.

    Returns
    -------
    tuple
        MNE-formatted events and the event id, that can be added
        via :func:`.raw.add_events(events)`, and a dictionary with event's names.

    See Also
    --------
    events_find

    Examples
    ----------
    .. ipython:: python

      import neurokit2 as nk

      signal = nk.signal_simulate(duration=4)
      events = nk.events_find(signal)
      events, event_id = nk.events_to_mne(events)
      events

      event_id

      # Conditions
      events = nk.events_find(signal, event_conditions=["A", "B", "A", "B"])
      events, event_id = nk.events_to_mne(events)
      event_id

    """

    if isinstance(events, dict):
        if "condition" in events.keys():
            event_conditions = events["condition"]
        events = events["onset"]

    event_id = {}

    if event_conditions is None:
        event_conditions = ["event"] * len(events)

    # Sanity check
    if len(event_conditions) != len(events):
        raise ValueError(
            "NeuroKit error: events_to_mne(): 'event_conditions' argument of different length than event onsets."
        )

    event_names = list(set(event_conditions))
    event_index = list(range(len(event_names)))
    for i in enumerate(event_names):
        event_conditions = [event_index[i[0]] if x == i[1] else x for x in event_conditions]
        event_id[i[1]] = event_index[i[0]]

    events = np.array([events, [0] * len(events), event_conditions]).T

    return events, event_id
