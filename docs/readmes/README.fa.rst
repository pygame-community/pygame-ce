.. image:: https://raw.githubusercontent.com/pygame-community/pygame-ce/main/docs/reST/_static/pygame_ce_logo.svg
  :alt: pygame
  :target: https://pyga.me/


|DocsStatus|
|PyPiVersion| |PyPiLicense|
|Python3| |GithubCommits| |BlackFormatBadge|

`English`_ `简体中文`_ `繁體中文`_ `Français`_ **فارسی** `Español`_ `日本語`_ `Italiano`_ `Русский`_

---------------------------------------------------------------------------------------------------
کتابخانه
Pygame_
برای توسعه دادن برنامه های چند رسانه ای
مانند بازی های رایانه ای, به کار می رود.

کتابخانه
pygame به عنوان زیرساخت های اصلی خود از کتابخانه
`Simple DirectMedia Layer library`_
استفاده می کند.


همچنین از کتابخانه های پرطرفدار و متعدد زیادی برای دسترسی
به پرکاربرد ترین الگوریتم ها استفاده می کند,
که در نتیجه این مسئله, فرایند تولید و توسعه برنامه
با استفاده از کتابخانه pygame خلاقانه تر و آسان تر می شود.


این توزیع با نام
**'pygame - Community Edition'** ('pygame-ce' برای اختصار)
شناخته می شود.

این توزیع یک فورک از نسخه آپ استریم (نسخه اصلی) کتابخانه pygame می باشد
که توسط مشارکت کنندگان (contributor) های سابق نسخه
آپ استریم در حال توسعه و نگهداری هست,
و بعد از رخ دادن چالش هایی حل نشدنی که همکاری در نسخه اصلی کتابخانه
را غیر ممکن می کرد, برای اولین بار ساخته شد.

این توزیع به عنوان اهداف خود, انتشار های سریع تر و بیشتر نسخه های پروژه, رفع ادامه دار باگ ها و بهینه سازی پروژه,
و کنترل کردن فرایند توسعه پروژه به صورت دموکراتیک
را مد نظر خود دارد.

ما به مشارکت کننده (contributor) هایی که علاقه مند به همکاری با
ما هستند خوش آمد میگوییم و از آنها به گرمی استقبال می کنیم!.



روش نصب
------------

::

   pip install pygame-ce


Help (کمک و راهنمایی)
----
اگر به تازگی قصد یادگیری کتابخانه pygame را دارید, می توانید به سادگی
این فرایند را آغاز کنید.
آموزش ها و معرفی های زیادی از کتابخانه pygame در اینترنت موجود هست.
همچنین اسناد ارجاعی کاملی برای این کتابخانه تهیه و تدوین شده است.
می توانید با استفاده از این لینک
`docs page`_
به اسناد ارجاعی دسترسی داشته باشید.

همچنین اگر کتابخانه pygame را نصب کرده اید می توانید با وارد کردن دستور

``python -m pygame.docs``

در فضای ترمینال یا کامند لاین سیستم عامل خود, به اسناد ارجاعی دسترسی داشته باشید.


اسناد ارجاعی کتابخانه پس از هر بروزرسانی نسخه توسعه داده شده در مخزن
pygame_ce_
آپدیت می شوند.

محتوای این اسناد ممکن است از نسخه ای از pygame که شما استفاده می کنید کمی جدید تر باشد.
برای آپگرید کردن pygame خود به آخرین ورژن, دستور زیر را در فضای کامند لاین اجرا کنید.

``pip install pygame-ce --upgrade``

همچنین پوشه ی examples شامل تعداد زیادی از برنامه ها قابل اجرا هست که
می توانید به سادگی با تغییر دادن آنها با قابلیت های کتابخانه آشنا بشوید.

Building From Source (ساخت و اجرا با استفاده از سرس کد)
--------------------

اگر می خواهید از قابلیت هایی که در حال توسعه هستند و هنوز به آخرین نسخه پروژه اضافه
نشده اند استفاده کنید, یا می خواهید در توسعه و نگه داری این پروژه مشارکت داشته باشید,
به جای نصب کردن کتابخانه روی سیستم عامل خود با استفاده از pip,
شما باید کتابخانه pygame را روی سیستم خود به صورت local بسازید (build بگیرید).

نصب کردن کتابخانه با استفاده از سرس کد تا حد زیادی اتوماتیک شد است.
اکثر کار هایی که در این فرایند انجام می شوند شامل کامپایل کردن و نصب کردن
تمام وابستگی (dependency) های پاگیم می باشد.
زمانی که این فرایند به پایان رسیده است, اسکریپت
``setup.py``
را اجرا کنید که تلاش میکند کتابخانه pygame را روی دستگاه شما پیکربندی (configure) و نصب کند.

برای کسب اطلاعات بیشتر در رابطه با فرایند نصب کردن و کامپایل کردن, می توانید به صفحه
`Compilation wiki page`_
مراجعه کنید.


Credits
-------

ما از تمام افرادی که در توسعه و نگه داری این پروژه اپن سرس
با ما همکاری کرده اند سپاس گذاری می کنیم.

همچنین قصد داریم تشکر ویژه ی خود را از افراد زیر اعلام کنیم.


* Marcus Von Appen: many changes, and fixes, 1.7.1+ freebsd maintainer
* Lenard Lindstrom: the 1.8+ windows maintainer, many changes, and fixes
* Brian Fisher for svn auto builder, bug tracker and many contributions
* Rene Dudfield: many changes, and fixes, 1.7+ release manager/maintainer
* Phil Hassey for his work on the pygame.org website
* DR0ID for his work on the sprite module
* Richard Goedeken for his smoothscale function
* Ulf Ekström for his pixel perfect collision detection code
* Pete Shinners: original author
* David Clark for filling the right-hand-man position
* Ed Boraas and Francis Irving: Debian packages
* Maxim Sobolev: FreeBSD packaging
* Bob Ippolito: macOS and OS X porting (much work!)
* Jan Ekhol, Ray Kelm, and Peter Nicolai: putting up with early design ideas
* Nat Pryce for starting our unit tests
* Dan Richter for documentation work
* TheCorruptor for his incredible logos and graphics
* Nicholas Dudfield: many test improvements
* Alex Folkner for pygame-ctypes


از افراد زیر بابت ارسال patch ها و تصحیح اشکالات پروژه تشکر می کنیم:
Niki Spahiev, Gordon
Tyler, Nathaniel Pryce, Dave Wallace, John Popplewell, Michael Urman,
Andrew Straw, Michael Hudson, Ole Martin Bjoerndalen, Herve Cauwelier,
James Mazer, Lalo Martins, Timothy Stranex, Chad Lester, Matthias
Spiller, Bo Jangeborg, Dmitry Borisov, Campbell Barton, Diego Essaya,
Eyal Lotem, Regis Desgroppes, Emmanuel Hainry, Randy Kaelber,
Matthew L Daniel, Nirav Patel, Forrest Voight, Charlie Nolan,
Frankie Robertson, John Krukoff, Lorenz Quack, Nick Irvine,
Michael George, Saul Spatz, Thomas Ibbotson, Tom Rothamel, Evan Kroske,
Cambell Barton.

همچنین از افرادی که در پیدا کردن باگ های پروژه به ما کمک کرده اند نیز قدردانی ویژه داریم:
Angus, Guillaume Proux, Frank
Raiser, Austin Henry, Kaweh Kazemi, Arturo Aldama, Mike Mulcheck,
Michael Benfield, David Lau


هنوز افراد بسیار بیشتری هستند که در توسعه این پروژه به ما کمک کرده اند,
ایده های جدیدی ارسال کرده اند, و نگه داری پروژه را ممکن ساخته اند.
زحمات شما زندگی توسعه دهندگی ما را آسان تر کرده است. از شما متشکریم!

از افرادی که در تهیه و تدوین اسناد ارجاعی در سایت pygame.org به ما کمک کرده اند متشکریم.

از تمام افرادی که با ساخت بازی های و متعدد و ارسال کردن آنها
در سایت pygame.org به دیگر کاربران جهت یادگیری و لذت بردن از آنها
کمک کرده اند نیز تشکر ویژه ای داریم.

تشکر های بسیاری نیز به Jame Paige بابت میزبانی کردن سرویس pygame در bugzilla بدهکاریم.


همچنین از Roger Dingledine و تیم SEUL.ORG بابت
میزبانی فوق العاده ای که بابت سایت pygame.org ارائه داده اند سپاس گذاری می کنیم.

Dependencies (وابستگی ها)
------------

**note:** This section translation is out of date (September 2023)

کتابخانه Pygame به وضوح به کتابخانه SDL و زبان Python وابسته است.
همچنین به چندین کتابخانه کوچکتر دیگر نیز لینک می‌شود و از آنها استفاده می‌کند.
ماژول فونت به کتابخانه SDL_ttf تکیه می کند که خود نیز به freetype وابسته است.
ماژول mixer و mixer.music هم به کتابخانه SDL_mixer وابستگی دارند.

ماژول image به SDL_image که می تواند به libjpeg و libpng وابستگی داشته باشد تکیه می کند.
ماژول transform نیز از نسخه ای جاسازی شده از SDL_rotozoom برای فانکش rotozoom خود استفاده می کند.

ماژول surfarray نیز از پکیج NumPy در زبان پایتون, برای پردازش آرایه های چندبعدی عددی خود
استفاده می کند.



در لیست زیر می توانید نسخه های دقیق هر یک از وابستگی های مورد نیاز را
مشاهده کنید.

+----------+------------------------+
| CPython  | >= 3.9 (Or use PyPy3)  |
+----------+------------------------+
| SDL      | >= 2.0.14              |
+----------+------------------------+
| SDL_mixer| >= 2.0.4               |
+----------+------------------------+
| SDL_image| >= 2.0.4               |
+----------+------------------------+
| SDL_ttf  | >= 2.0.15              |
+----------+------------------------+



License
-------
LGPL-2.1-or-later **شناسه مجوز:**

این کتابخانه با استفاده از
`GNU LGPL version 2.1`_
لایسنس شده است که در فایل
``docs/LDGP.txt``
قابل دسترس هست.
ما حق تغییر دادن این لایسنس را در نسخه های آینده این کتابخانه رزرو می کنیم.

این مسئله در اختصار به این معنی است که شما می توانید از کتابخانه pygame در
تمام پروژه های خود استفاده کنید. اما اگر تغییری در سرس کد pygame ایجاد کنید,
آن تغییرات باید با لایسنسی که با لایسنس pygame سازگار است منتشر شوند. (ترجیحا
ارجاع داده شده به pygame).
انتشار بازی هایی که متن بسته و بازی هایی که منجر به درآمد زایی می شوند مجاز است.

تمام برنامه های داخل پوشه
``examples``
شامل اموال عمومی‌ (public domain) می شوند.

برای اطلاعات بیشتر در مورد لایسنس هر وابستگی (dependency),
فایل docs/licenses را مشاهده کنید.


.. |PyPiVersion| image:: https://img.shields.io/pypi/v/pygame-ce.svg?v=1
   :target: https://pypi.python.org/pypi/pygame-ce

.. |PyPiLicense| image:: https://img.shields.io/pypi/l/pygame-ce.svg?v=1
   :target: https://pypi.python.org/pypi/pygame-ce

.. |Python3| image:: https://img.shields.io/badge/python-3-blue.svg?v=1

.. |GithubCommits| image:: https://img.shields.io/github/commits-since/pygame-community/pygame-ce/2.3.0.svg
   :target: https://github.com/pygame-community/pygame-ce/compare/2.3.0...main

.. |DocsStatus| image:: https://img.shields.io/website?down_message=offline&label=docs&up_message=online&url=https%3A%2F%2Fpyga.me%2Fdocs%2F
   :target: https://pyga.me/docs/

.. |BlackFormatBadge| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. _pygame: https://pyga.me
.. _Simple DirectMedia Layer library: https://www.libsdl.org
.. _Compilation wiki page: https://github.com/pygame-community/pygame-ce/wiki#compiling
.. _docs page: https://pyga.me/docs
.. _GNU LGPL version 2.1: https://www.gnu.org/copyleft/lesser.html
.. _pygame_ce: https://github.com/pygame-community/pygame-ce

.. _English: ./../../README.rst
.. _简体中文: README.zh-cn.rst
.. _繁體中文: README.zh-tw.rst
.. _Français: README.fr.rst
.. _Español: README.es.rst
.. _日本語: README.ja.rst
.. _Italiano: README.it.rst
.. _Русский: README.ru.rst
