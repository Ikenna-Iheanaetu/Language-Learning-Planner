# Creating a Good Pull Request

## Pull Request Title
- **Good Example:** "Implement time allocation algorithm for language skills"
- **Bad Example:** "Fixed stuff"

## Pull Request Description Template
```markdown
## Description
[Brief description of what this PR accomplishes]

## Changes Made
- [Change 1]
- [Change 2]
- [Change 3]

## Testing Done
[Describe how you tested your changes]

## Screenshots (if relevant)
[Add screenshots if applicable]
```

## Example pull request


## Description
This PR implements the core time allocation algorithm that distributes study time across different language skills based on user goals and language difficulty.

## Changes Made
- Added `time_allocation.py` with the formula implementation
- Created unit tests for the algorithm
- Updated `inference_engine.py` to use the new algorithm
- Added documentation for the time allocation parameters

## Testing Done
- Tested with different input scenarios (beginner/advanced, various time constraints)
- Verified outputs against expected distributions
- All unit tests passing
