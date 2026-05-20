from django.db import migrations


def forwards(apps, schema_editor):
    Household_Information = apps.get_model('believer', 'Household_Information')
    Member_Information = apps.get_model('believer', 'Member_Information')

    households = {
        household.Household_ID: household
        for household in Household_Information.objects.all()
    }

    for member in Member_Information.objects.filter(Household__isnull=True):
        household = None
        member_id = member.Member_ID or ''

        if 'M' in member_id:
            candidate = member_id.rsplit('M', 1)[0]
            household = households.get(candidate)

        if household is None:
            household = Household_Information.objects.filter(
                Head_of_Household_ID=member_id
            ).first()

        if household is not None:
            member.Household = household
            member.save(update_fields=['Household'])


def backwards(apps, schema_editor):
    Member_Information = apps.get_model('believer', 'Member_Information')
    Member_Information.objects.update(Household=None)


class Migration(migrations.Migration):
    dependencies = [
        ('believer', '0002_remove_member_information_household_id_and_more'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
