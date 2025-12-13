from django.contrib.auth.models import User
from accounts.models import Profile

if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    # Signal should have created profile, but let's ensure role is admin
    if hasattr(user, 'profile'):
        user.profile.role = 'admin'
        user.profile.save()
    else:
        # Fallback if signal didn't run (though it should)
        Profile.objects.create(user=user, role='admin')
    print("Superuser 'admin' created with password 'admin123'")
else:
    print("User 'admin' already exists")
