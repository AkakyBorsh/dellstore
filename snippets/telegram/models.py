from attr import attrs, attrib


@attrs()
class SendMessage:
    ok = attrib(type=bool)
    result = attrib(type=dict)
