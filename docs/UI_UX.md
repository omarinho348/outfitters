# UI_UX.md

Status: **not yet designed in detail.** This is the working spec, refined in
Phase 1/4 as real screens get built.

## Navigation (proposed, to validate during Phase 4 build)

Bottom tabs: **Home · Closet · [+ Add] · Outfits · Shop**
Center "+" as a raised action button opening a sheet: Add Clothing / Create
Outfit / Post Inspiration — not a plain tab.

## Screen List (MVP)

- Auth: Login, Register
- Home: dashboard/discovery surface (summarizes, doesn't duplicate other tabs)
- Closet: grid view, filters, search, item detail, add/edit item
- Add flow: camera/gallery picker → AI analysis result → confirm/edit → save
- Outfit builder: item picker by category → preview → save/post
- AI Stylist: NL input + structured filters → generated outfit results
- Outfits (social feed): scrollable feed, post detail, profile view
- Shop: brand list, product grid, product detail (external link out)
- Outfit completion: results shown as "missing piece" + matched products
- Profile: own profile, followers/following, saved posts

## Design Direction

Fashion-forward, image-first, youthful but not childish. Avoid: default
component styling, generic card grids with no visual hierarchy, dense text.
Reference feel: Depop/Pinterest density for browsing, clean minimal chrome
around imagery.

## Design Tokens (to finalize in Phase 1 before component build)

- **Color:** neutral base (near-black/near-white) + one accent color TBD;
  avoid default RN/Expo blue.
- **Type scale:** to define — likely a single expressive display font for
  headings, clean system font for body (perf + readability).
- **Spacing scale:** 4/8/12/16/24/32 px system.
- **Components:** Button, Input, ClothingCard, OutfitCard, ProductCard,
  ProfileHeader, BottomNav, Chip (for tags/filters), Modal/Sheet.

Actual token values (hex codes, font choices) to be decided visually during
Phase 1, not guessed here — will use `frontend-design` skill guidance when
building real components in Phase 4.

## Accessibility Baseline

Minimum tap target 44x44pt, contrast checked against WCAG AA, meaningful
error copy (no raw stack traces), screen-reader labels on icon-only buttons.