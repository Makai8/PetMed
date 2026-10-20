# Business Rules 
1. Each user must have a unique email address.
2. Each user must be assigned at least one valid system role.
3. If PetMed supports multiple roles per user, role assignments must be stored through a user-role relationship rather than a single role field.
4. Roles may have multiple permissions, and permissions may belong to multiple roles.
5. Only users with the required permissions may perform restricted actions such as moderation, professional verification, or system administration.
6. Administrator accounts should not be created through normal public registration.
7. A professional profile must belong to one valid user account.
8. Veterinarian and Pet Health Expert privileges must remain inactive until the professional account is verified.
9. Only authorized Administrators may approve, reject, suspend, or revoke professional verification.
10. Each pet must belong to exactly one Pet Owner, while a Pet Owner may own multiple pets.
11. All pet-health records must reference a valid pet.
12. A pet may have multiple allergy, condition, symptom, treatment, and medication records.
13. A symptom log must record the pet, the symptom, and when it was observed.
14. A treatment may optionally reference the professional who prescribed or recommended it.
15. A medication record must belong to one pet and should include dosage, frequency, and treatment dates when applicable.
16. A reminder must belong to a valid pet and user, and may reference a medication record when appropriate.
17. A veterinary referral must belong to a valid pet and identify the professional who created it.
18. Pet-health data shared with a professional must be covered by a valid data-sharing authorization when authorization is required.
19. Revoked or expired data-sharing authorization must no longer grant access to protected pet-health information.
20. Every community post and health article must belong to one valid author.
21. Posts and articles may have multiple tags, and many-to-many relationships must be handled through associative entities such as POST_TAG and ARTICLE_TAG.
22. Each comment must belong to a valid post and a valid user.
23. A reply comment may reference another comment as its parent.
24. A user may like or save the same post only once.
25. A user may follow another user only once and may not follow themselves.
26. Each health question must belong to a valid user and may optionally reference a specific pet.
27. Each advice response must belong to one health question and identify the user who authored it.
28. Professional guidance may only be labeled as Veterinarian or Pet Health Expert guidance when the author has the appropriate verified professional status.
29. Every message must identify a valid sender and recipient.
30. Every notification must belong to a valid user and should record whether it has been read.
31. Each product must have a unique product identifier and may be marked inactive instead of permanently deleted.
32. Each product review must belong to one valid product and one valid user.
33. Product ratings must fall within the rating range approved by the application.
34. A user should have no more than one active review for the same product unless multiple reviews are intentionally supported.
35. Every report must identify the user who submitted it and the reported post, comment, or user when applicable.
36. Each moderation case must reference a valid report and may be assigned to one moderator.
37. Every moderation action must belong to a moderation case and identify the moderator or administrator who performed it.
38. Closed moderation cases should remain stored for audit and history purposes.
39. Medication reference records should preserve important safety information such as warnings, source information, and last-reviewed date when available.
40. Each system-setting key must be unique, and only authorized administrators may modify system settings.
41. Every primary key must uniquely identify one record.
42. Every required foreign key must reference an existing valid record.
43. The database must prevent orphaned records.
44. Important historical records should generally be archived, revoked, closed, or deactivated instead of permanently deleted when audit history is needed.
45. Date values must remain logically consistent, such as preventing an end date from occurring before a start date.
46. Status fields such as user status, verification status, report status, reminder status, and moderation-case status must use valid values defined by the system.
