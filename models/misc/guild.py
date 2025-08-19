from tortoise import fields
from tortoise.models import Model
import config as cfg

class Guild(Model):
    """Represents the settings for a guild in the database."""

    # The primary key for this table will be the Discord Guild's ID.
    # We use BigIntField because Discord IDs are very large numbers.
    id = fields.BigIntField(pk=True)

    # This field will store the custom command prefix for the guild.
    # It can be up to 10 characters long.
    # If a guild doesn't have a custom prefix set, it will use the default
    # from your config file.
    prefix = fields.CharField(max_length=10, default=cfg.PREFIX)

    def __str__(self):
        return f"Guild(id={self.id}, prefix='{self.prefix}')"

    class Meta:
        # This sets the name of the database table.
        table = "guilds"
