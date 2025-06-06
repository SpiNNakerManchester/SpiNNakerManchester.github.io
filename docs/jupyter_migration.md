---
title: Jupyter Migration
---

# Introduction
The original Jupyter service is now out-of-date and has a number of security issues that can only be addressed by updating the software.  The way in which the service uses persistent images, although it means continuous compatibility for users, it makes it very difficult to update anything once an image has been created.  This also makes it more difficult for users to update to a new version of the software without some manual intervention on their side or ours.  For this reason, we have created a new service, but with some changes detailed below.  Also below are some instructions on what you need to do to migrate to the new server.

# Important Information
Useful information about the new service on https://sands.cs.man.ac.uk:
 
 - Only files in ``work`` or ``drive`` will be persisted.  All other files will be deleted when you log out (or when inactive sessions time out - timing of this is to be determined).
 - You can install things as before, but these are not persisted between sessions.  It is therefore recommended to install additional libraries via [ipython magics](https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-pip), so that they will be reinstalled on next execution.
 - Your workspace will be restored on execution to the extent that open files that are in persistent storage will be reopened.
 - The new Jupyter has been set up with 3 Kernels:
     - sPyNNaker_7.2.1 and sPyNNaker_7.3.0 are the latest releases of the software.  As more releases are done, you will see them appear on the next log in as new Kernels.
     - sPyNNakerGit has access to the Git repositories of the software, so contains the absolute latest versions of everything.  This will be updated periodically.
 - The NRP is no longer installed having gone out of support.
 - You can now log in using a Google Login if you don't have an EBRAINS login, but the EBRAINS drive will then of course not be available (and Google Drive integration is not supported at this time).

# Migration
All files that were available on the original service should be available to you provided you log in with the same user id.  These will be visible as follows:

 - ``oldwork``: This contains the read-only contents of your original ``work`` folder.
 - ``oldjupyter``: This is the whole of your container image that was running on the old service.  Depending on how old your image was, this may contain the following likely most useful folders:
     - ``home/bbnrpsoa``: If you image is more recent and included NRP support, this will be your original home folder.
     - ``home/spinnaker``: This may be your original home folder if your image is older.
     - ``home/jovyan``: This is related to how the image was built; it is unlikely to contain anything useful.
     - Most other folders here are likely to contain system data rather than anything useful, but are included just in case.

Please copy anything useful out of these folders on to either your own computer, or else in to the ``work`` or ``drive`` folders.

