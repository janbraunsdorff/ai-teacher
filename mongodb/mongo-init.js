db.auth('admin_user', 'admin_pass');
db = db.getSiblingDB('teacher');
db.createUser({
  user: 'application_user',
  pwd: 'application_pass',
  roles: [
    {
      role: 'readWrite',
      db: 'teacher',
    },
  ],
});
