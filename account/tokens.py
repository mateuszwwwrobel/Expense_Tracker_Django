from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """Token Generator class for user account activation."""

    def _make_hash_value(self, user, timestamp):
        """Create a hash value."""
        return six.text_type(user.pk) + six.text_type(timestamp)


account_activation_token = AccountActivationTokenGenerator()
