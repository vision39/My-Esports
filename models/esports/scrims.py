from tortoise import fields
from tortoise.models import Model
import datetime

class Scrim(Model):
    """Represents a scrim event in the database, with full customization options."""

    # --- Core Fields ---
    id = fields.IntField(pk=True)
    guild_id = fields.BigIntField()
    host_id = fields.BigIntField()
    
    # --- Scrim Details ---
    title = fields.CharField(max_length=200)
    scrim_time = fields.DatetimeField()
    scrim_days = fields.CharField(max_length=100, default="Mo, Tu, We, Th, Fr, Sa, Su")
    
    # --- Registration Details ---
    total_slots = fields.IntField(default=25)
    is_open = fields.BooleanField(default=True)
    
    # --- Channel and Message IDs ---
    reg_channel_id = fields.BigIntField(null=True)
    slotlist_channel_id = fields.BigIntField(null=True) # <-- NEW FIELD
    reg_message_id = fields.BigIntField(null=True)
    log_channel_id = fields.BigIntField(null=True)

    # --- Role IDs ---
    ping_role_id = fields.BigIntField(null=True)
    success_role_id = fields.BigIntField(null=True) # <-- NEW FIELD
    
    # --- Data Storage (JSON) ---
    registered_teams = fields.JSONField(default=list)
    reserves = fields.JSONField(default=list)
    banned_users = fields.JSONField(default=list)

    # --- Customization Fields ---
    open_message = fields.TextField(null=True, default="Registration is now open!")
    dm_message = fields.TextField(null=True, default="You have successfully registered for {scrim_title}.")
    
    class Meta:
        table = "scrims"

    def __str__(self):
        return f"Scrim(id={self.id}, title='{self.title}')"
