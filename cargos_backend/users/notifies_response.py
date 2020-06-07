from django.urls import reverse

from bridge.database_queries import get_notifications_unread_first


def notifies_response(user, notify_pk, ignore=None):
    notifies = get_notifications_unread_first(user)
    notifies_as_table_unread = []
    notifies_as_table_read = []

    for notif in notifies:
        if notif.pk == int(notify_pk):
            if ignore is None:
                notif.deleted = True
                notif.save()
                continue
            else:
                notif.unread = False if ignore == 'true' else True
                notif.save()

        dct = notif.__dict__
        dct['actor'] = str(notif.actor) if notif.actor else None
        dct['recipient'] = str(notif.recipient) if notif.recipient else None
        dct['link_notify'] = reverse('users:notification_single', kwargs={'pk': notif.id})

        if notif.actor:
            dct['link_cargo'] = reverse('preview_cargo', kwargs={'pk': notif.actor.id})

        del dct['_state']

        if notif.unread:
            notifies_as_table_unread.append(dct)
        else:
            notifies_as_table_read.append(dct)
    return notifies_as_table_unread, notifies_as_table_read
