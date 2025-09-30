from django import template

register = template.Library()

@register.filter
def sortSectionByDayOfWeek(sections):
    for section in sections:
        section.day_of_week_num = section.dayOfWeek()
    return sections

@register.filter
def formatPhoneNumber(value):
    if not value:
        return ""
    s = str(value)
    # ถ้าเบอร์มี 10 หลัก
    if len(s) == 10:
        return f"{s[:3]}-{s[3:6]}-{s[6:]}"
    return value