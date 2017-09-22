from django import template


register = template.Library()


@register.inclusion_tag('main/templatetags/circle_item.html')
def marketing__circle_item(img_name: str):
    items = {
        'yoda.jpg': {
            'img': img_name,
            'heading': 'Hone your Jedi Skills',
            'caption': "All members have access to our unique training and"
                       " achievements ladders. Progress through the levels and"
                       " show everyone who the top Jedi Master is!",
            'button_title': 'Sign Up Now &raquo;'
        },
        'clone-army.png': {
            'img': img_name,
            'heading': 'Build your Clan',
            'caption': "Engage in meaningful conversation, or bloodthirsty battle!"
                       " If it's related to Star Wars, in any way, you better"
                       " believe we do it here.",
            'button_title': 'Sign Up Now &raquo;'
        },
        'leia.jpg': {
            'img': img_name,
            'heading': 'Find Love',
            'caption': "Everybody knows Star Wars fans are the best mates for"
                       " Star Wars fans. Find your Princess Leia or Han Solo and"
                       " explore the stars together.",
            'button_title': 'Sign Up Now &raquo;'
        },
    }
    return items[img_name]
