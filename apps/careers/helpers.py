import jingo

from django_jobvite.models import Position, Category


@jingo.register.filter
def columnize(data, n):
    """
    Split job listings into separate lists so we can display them
    in a multi-column layout. Try to even out the distribution as
    much as possible.
    """
    ncategories = Category.objects.all().count()
    npositions = Position.objects.all().count()

    header_height = 1.2
    columns = [{} for i in range(0, n)]
    cursor = 0
    height = 0
    max_height = ((ncategories * header_height + npositions) / 3.0) + 5

    for category, positions in iter(sorted(data.iteritems())):
        height += header_height + len(positions)

        if height > max_height:
            cursor += 1
            columns[cursor][category] = positions
            height = header_height + len(positions)
            continue
        columns[cursor][category] = positions
    return columns
