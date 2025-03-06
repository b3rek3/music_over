import csv
import re
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from review.models import Song, Album, Comment, BandMember


class Command(BaseCommand):
    help = 'Load data from a CSV file into the database.'

    def add_arguments(self, parser):
        parser.add_argument('--csv', type=str, help='Path to the CSV file')

    @staticmethod
    def row_to_dict(row, header):
        """Convert a CSV row into a dictionary using the header as keys."""
        if len(row) < len(header):
            row += [''] * (len(header) - len(row))
        return dict(zip(header, row))

    @staticmethod
    def fix_date(date_str):
        """Convert date from various formats to 'YYYY-MM-DD'."""
        for fmt in ("%d-%m-%Y", "%m-%d-%Y", "%Y-%m-%d"):  # Common formats
            try:
                return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
        return date_str  # Return as is if no format matches

    @staticmethod
    def convert_duration(duration_str):
        """Convert duration from 'MM:SS' format to timedelta."""
        try:
            minutes, seconds = map(int, duration_str.split(":"))
            return timedelta(minutes=minutes, seconds=seconds)
        except (ValueError, AttributeError):
            print(f"Warning: Invalid duration format '{duration_str}', setting to 00:00")
            return timedelta()  # Default to 0 if parsing fails

    def handle(self, *args, **options):
        m = re.compile(r'content:(\w+)')  # Pattern to detect model name
        header = None
        models = {}

        # Read CSV file
        try:
            with open(options['csv'], encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if max(len(cell.strip()) for cell in row[1:] + ['']) == 0 and m.match(row[0]):
                        model_name = m.match(row[0]).groups()[0]
                        models[model_name] = []
                        header = None
                        continue

                    if header is None:
                        header = row
                        continue

                    row_dict = self.row_to_dict(row, header)
                    if set(row_dict.values()) == {''}:
                        continue
                    models[model_name].append(row_dict)

        except FileNotFoundError:
            raise CommandError(f'File "{options["csv"]}" does not exist')

        # Process Band Members
        for data in models.get('BandMember', []):
            member, created = BandMember.objects.get_or_create(
                name=data['member_name'],
                defaults={'role': data['member_role']}
            )
            if created:
                print(f'Created Band Member: {member.name}')

        # Process Albums (with date fix)
        for data in models.get('Album', []):
            fixed_date = self.fix_date(data['album_release_date'].replace('/', '-'))
            album, created = Album.objects.get_or_create(
                title=data['album_title'],
                defaults={
                    'release_date': fixed_date,
                    'cover_image': data['album_cover_image']
                }
            )
            if created:
                print(f'Created Album: {album.title}')

        # Process Songs (Ensure album exists before adding songs)
        for data in models.get('Song', []):
            album_title = data['song_album']
            try:
                album = Album.objects.get(title=album_title)
            except Album.DoesNotExist:
                print(f'Error: Album "{album_title}" not found for song "{data["song_title"]}". Skipping.')
                continue  # Skip songs with missing albums

            song, created = Song.objects.get_or_create(
                title=data['song_title'],
                album=album,  # Ensure album exists
                defaults={'duration': self.convert_duration(data['song_duration'])}  # Convert duration
            )
            if created:
                print(f'Created Song: {song.title}')

        # Process Comments
        for data in models.get('Comment', []):
            try:
                song = Song.objects.get(title=data['comment_song'])
                comment, created = Comment.objects.get_or_create(
                    text=data['comment_content'],
                    song=song,
                    created_at={'date_posted': self.fix_date(data['comment_date'])}
                )
                if created:
                    print(f'Created Comment on "{song.title}": {comment.content[:30]}...')
            except Song.DoesNotExist:
                print(f'Error: Song "{data["comment_song"]}" not found for comment.')

        print("Database import complete!")
