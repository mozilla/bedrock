# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.urls import reverse

from wagtail import hooks
from wagtail.admin.menu import MenuItem


@hooks.register("register_admin_menu_item")
def register_task_queue_link():
    return MenuItem(
        "Task Queue",
        reverse("rq_home"),
        icon_name="tasks",
        order=80000,
    )


@hooks.register("register_admin_menu_item")
def register_django_admin_link():
    return MenuItem(
        "Django Admin",
        reverse("admin:index"),
        icon_name="tasks",
        order=80001,
    )
