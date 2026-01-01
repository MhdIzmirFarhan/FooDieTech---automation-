# Copilot Instructions for autoComplete Project

## Project Overview
This is a Playwright-based browser automation script that automates creating food items on the foodiee.com.my platform. The script handles form filling after manual login and captcha solving.

## Architecture
- Single Python script (`main.py`) using Playwright's sync API
- Launches Chromium browser in non-headless mode for manual captcha interaction
- Automates form submission with predefined values for a "Masala Dosai" item

## Key Dependencies
- `playwright` - For browser automation and web scraping
- Install with: `pip install playwright` then `playwright install`

## Developer Workflows
- **Running the script**: `python main.py`
- **Manual steps required**: Login to the website and solve captcha before pressing Enter
- **Debugging**: Browser runs in visible mode (`headless=False`) with `slow_mo=80` for step-by-step observation

## Code Patterns
- **Select2 dropdowns**: Use `page.click("select[name='field'] + span.select2")` followed by clicking `.select2-results__option`
- **Multi-select handling**: For arrays like `food_sessions[]`, click all options in the dropdown
- **Form fields**: Direct selectors like `input[name='foodname']`, `input[name='foodprice']`
- **Checkbox groups**: Loop through values for `input[name='menutype[]'][value='X']`
- **Submission**: Standard `button[type='submit']` click

## Specific Examples
- Category selection: Targets `data-select2-id*='1'` for "Juice Items"
- Kitchen selection: Clicks first available option in dropdown
- Menu types: Checks all values 1-5 (Breakfast, Lunch, Dinner, etc.)
- Food sessions: Selects all available session options
- Status: Sets to "1" (Active)

## Integration Points
- External website: https://srivasanthavilash.foodiee.com.my/itemmanage/item_food/create
- Requires manual authentication and captcha bypass
- No API integration; pure browser automation

## Conventions
- Hardcoded item details in script (name: "Masala Dosai", price: "6.50")
- Uses `time.sleep()` for brief pauses during multi-select operations
- Browser closes automatically after 5-second wait post-submission