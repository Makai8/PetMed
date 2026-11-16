// ------------------------------------------------------------
// Role settings: landing page, label and menu for each role.
// Role names match the Role table in the database (seed.sql).
// Menu items come from the PetMed Functional Requirements.
// "path" is set only on the Sprint IV use case for that role.
// ------------------------------------------------------------

export const roles = {
  pet_owner: {
    label: 'Pet Owner',
    home: '/owner',
    welcome: 'Keep your pets healthy and connect with the community.',
    menu: [
      { icon: '📰', title: 'Community Feed', text: 'Browse pet health posts and discussions.', path: '/owner/feed' },
      { icon: '🐶', title: 'My Pets', text: 'Create and update pet profiles.' },
      { icon: '✏️', title: 'Create Post', text: 'Share a question or experience.' },
      { icon: '🩺', title: 'Symptom Tracker', text: 'Record symptoms and health events.' },
      { icon: '💊', title: 'Medications and Reminders', text: 'Track treatments and doses.' },
      { icon: '❓', title: 'Ask for Health Advice', text: 'Ask the community, a vet or an expert.' },
      { icon: '🔎', title: 'Search Health Information', text: 'Symptoms, conditions and medications.' },
      { icon: '🛒', title: 'Products and Treatments', text: 'View approved pet health products.' },
      { icon: '⭐', title: 'Rate and Review', text: 'Review advice and products.' },
      { icon: '🎓', title: 'Request a Professional Role', text: 'Apply to be a vet, expert, moderator or admin.', path: '/request-role' },
    ],
  },
  veterinarian: {
    label: 'Veterinarian',
    home: '/vet',
    welcome: 'Review questions and guide pet owners with trusted advice.',
    menu: [
      { icon: '❓', title: 'Pet Health Questions', text: 'View questions submitted by pet owners.', path: '/vet/questions' },
      { icon: '🩺', title: 'Provide Guidance', text: 'Answer questions with general guidance.' },
      { icon: '📚', title: 'Publish Educational Content', text: 'Write posts on care and prevention.' },
      { icon: '📈', title: 'Symptom History', text: 'Review shared symptom records.' },
      { icon: '💊', title: 'Medication Review', text: 'Review recorded medications.' },
      { icon: '🏥', title: 'In Person Referrals', text: 'Refer owners to a clinic visit.' },
      { icon: '💬', title: 'Professional Discussion', text: 'Comment and connect with peers.' },
      { icon: '🚩', title: 'Report Unsafe Advice', text: 'Flag dangerous or misleading content.' },
    ],
  },
  pet_health_expert: {
    label: 'Pet Health Expert',
    home: '/expert',
    welcome: 'Share guidance within your approved area of expertise.',
    menu: [
      { icon: '🔎', title: 'Questions in My Expertise', text: 'Browse posts in your specialty.', path: '/expert/questions' },
      { icon: '🪪', title: 'Expertise Profile', text: 'Specialty, credentials and experience.' },
      { icon: '💡', title: 'Answer Specialty Questions', text: 'Respond within your area.' },
      { icon: '📚', title: 'Publish Educational Content', text: 'Write articles and tips.' },
      { icon: '🌿', title: 'Recommend Resources', text: 'Suggest approved wellness resources.' },
      { icon: '⭐', title: 'Product Feedback', text: 'Review user product experiences.' },
      { icon: '🏥', title: 'Flag for a Vet', text: 'Send out of scope concerns to a vet.' },
      { icon: '🚩', title: 'Report Content', text: 'Flag false or unsafe claims.' },
    ],
  },
  community_moderator: {
    label: 'Community Moderator',
    home: '/moderator',
    welcome: 'Keep the PetMed community safe and constructive.',
    menu: [
      { icon: '🚩', title: 'Reported Posts and Advice', text: 'View content reported by users.', path: '/moderator/reports' },
      { icon: '💬', title: 'Moderate Comments', text: 'Review reported comments.' },
      { icon: '👤', title: 'Reported Users', text: 'Review reports about users.' },
      { icon: '📁', title: 'Moderation Cases', text: 'Create, track and close cases.' },
      { icon: '⚠️', title: 'Warn or Restrict Users', text: 'Issue warnings and restrictions.' },
      { icon: '⬆️', title: 'Escalate Concerns', text: 'Send safety issues to an admin.' },
    ],
  },
  administrator: {
    label: 'Administrator',
    home: '/admin',
    welcome: 'Manage users, professionals and platform settings.',
    menu: [
      { icon: '👥', title: 'Manage Users', text: 'Search and list user accounts.', path: '/admin/users' },
      { icon: '✅', title: 'Role Requests', text: 'Approve vets, experts, moderators and admins.', path: '/admin/role-requests' },
      { icon: '🔐', title: 'Roles and Permissions', text: 'Assign role permissions.' },
      { icon: '🏷️', title: 'Health Categories and Tags', text: 'Maintain categories and tags.' },
      { icon: '💊', title: 'Products and Medications', text: 'Maintain approved product info.' },
      { icon: '🗂️', title: 'Platform Content', text: 'Review and remove content.' },
      { icon: '🚩', title: 'Reported Activity', text: 'Review escalated cases.' },
      { icon: '📊', title: 'Analytics and Reports', text: 'Generate platform reports.' },
      { icon: '⚙️', title: 'System Settings', text: 'Pet types, reminder rules and more.' },
    ],
  },
}
