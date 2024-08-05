.. include:: common.txt

:mod:`pygame.system`
======================

.. module:: pygame.system
    :synopsis: pygame module to provide additional context about the system

| :sl:`pygame module to provide additional context about the system`

.. versionadded:: 2.2.0

.. function:: get_cpu_instruction_sets

   | :sl:`get the information of CPU instruction sets`
   | :sg:`get_cpu_instruction_sets() -> instruction_sets`

   Returns a dict of the information of CPU instruction sets. The keys of
   the dict are the names of instruction sets and the values determine 
   whether the instruction set is available.

   Some of functions like ``Surface.blit`` can be accelerated by SIMD 
   instruction sets like SSE2 or AVX2. By checking the availability of 
   instruction sets, you can check if these accelerations are available.

   Here is an example of the returned dict
   ::

     {
          'ALTIVEC': False,
          'MMX': True,
          'SSE': True,
          'SSE2': True,
          'SSE3': True,
          'SSE41': True,
          'SSE42': True,
          'AVX': True,
          'AVX2': True, 
          'AVX512F': False,
          'NEON': False, 
          'ARMSIMD': False,
          'LSX': False, 
          'LASX': False
     }

   .. Note:: The value of ``ARMSIMD`` will be always False if
      SDL version < 2.0.12.
      
      The values of ``LSX`` and ``LASX`` will be always False if
      SDL version < 2.24.0.
   
   .. versionadded:: 2.3.1

    .. versionchanged:: 2.4.0 removed ``RDTSC`` key, 
        as it has been removed in pre-release SDL3

.. function:: get_total_ram

   | :sl:`get the amount of RAM configured in the system`
   | :sg:`get_total_ram() -> ram_size`

   Returns the amount of RAM configured in the system in MiB.

   .. versionadded:: 2.3.1

.. function:: get_pref_path

   | :sl:`get a writeable folder for your app`
   | :sg:`get_pref_path(org, app) -> path`

   When distributing apps, it's helpful to have a way to get a writeable path,
   because it's what apps are expected to do, and because sometimes the local
   space around the app isn't writeable to the app.

   This function returns a platform specific path for your app to store
   savegames, settings, and the like. This path is unique per user and
   per app name.

   It takes two strings, ``org`` and ``app``, referring to the "organization"
   and "application name." For example, the organization could be "Valve," 
   and the application name could be "Half Life 2." It then will figure out the
   preferred path, **creating the folders referenced by the path if necessary**,
   and return a string containing the absolute path.

   For example::

        On Windows, it would resemble
        C:\\Users\\bob\\AppData\\Roaming\\My Company\\My Program Name\\

        On macOS, it would resemble
        /Users/bob/Library/Application Support/My Company/My Program Name/

        And on Linux it would resemble
        /home/bob/.local/share/My Company/My Program Name/

   .. note::
        Since the organization and app names can potentially be used as
        a folder name, it is highly encouraged to avoid punctuation.
        Instead stick to letters, numbers, and spaces.

   .. note::
        The ``appdirs`` library has similar functionality for this use case,
        but has more "folder types" to choose from.
    
   .. versionadded:: 2.2.0

.. function:: get_pref_locales

   | :sl:`get preferred locales set on the system`
   | :sg:`get_pref_locales() -> list[locale]`

   Returns a list of "locale" dicts, sorted in descending order of preference
   set on the host OS (the most preferred locale is the first element). May
   also be an empty list if pygame could not find this information.

   Each "locale" dict contains the language code which can be accessed by the
   key ``"language"``. This language code is an ISO-639 language specifier 
   (such as "en" for English, "de" for German, etc).
   A "locale" dict may also optionally contain a ``"country"`` field, whose
   value is an ISO-3166 country code (such as "US" for the United States, 
   "CA" for Canada, etc). If this field is not set or undetermined, it is 
   ``None``.
   A "locale" dict which looks like ``{'language': 'en', 'country': 'US'}``
   indicates the user prefers American English, while
   ``{'language': 'en', 'country': None}`` indicates that the user prefers
   English, generically.

   This might be a bit of an expensive call because it has to query the OS. So
   this function must not be called in a game loop, instead it's best to ask 
   for this once and save the results. However, this list can change when the
   user changes a system preference outside of your program. pygame will send
   a ``LOCALECHANGED`` event in this case, if possible, and you can call this
   function again to get an updated copy of preferred locales.

   .. versionadded:: 2.2.0

.. function:: get_power_state

   | :sl:`get the current power supply state`
   | :sg:`get_pref_power_state() -> PowerState`

   **Experimental:** feature available for testing and feedback.
   We don't anticipate it changing, but it might if something important
   is brought up. `Please leave get_power_state feedback with 
   authors <https://github.com/pygame-community/pygame-ce/pull/2257>`_

   Returns a ``PowerState`` object representing the power supply state.
   
   Returns ``None`` if the power state is unknown.

   The PowerState object has several attributes:

   .. code-block:: text

        battery_percent:
            An integer between 0 and 100, representing the percentage of
            battery life left.

        battery_seconds:
            An integer, representing the seconds of battery life left.
            Could be None if the value is unknown.
    
        on_battery:
            True if the device is running on the battery (not plugged in).

        no_battery:
            True if the device has no battery available (plugged in).

        charging:
            True if the device is charging battery (plugged in).

        charged:
            True if the battery of the device is fully charged (plugged in).

        plugged_in:
            True if the device is plugged in.
            Equivalent to `not on_battery`.

        has_battery:
            True if the device has battery.
            Equivalent to `on_battery or not no_battery`.


   You should never take a battery status as absolute truth. Batteries
   (especially failing batteries) are delicate hardware, and the values
   reported here are best estimates based on what that hardware reports. It's
   not uncommon for older batteries to lose stored power much faster than it
   reports, or completely drain when reporting it has 20 percent left, etc.

   Battery status can change at any time; if you are concerned with power
   state, you should call this function frequently, and perhaps ignore changes
   until they seem to be stable for a few seconds.

   It's possible a platform can only report battery percentage or time left
   but not both.

   .. versionadded:: 2.4.0
