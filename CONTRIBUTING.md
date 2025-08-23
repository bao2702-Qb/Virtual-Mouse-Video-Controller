# Contributing to Virtual Mouse with Video Control

Thank you for your interest in contributing to this project! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)
- [Feature Requests](#feature-requests)
- [Questions and Discussions](#questions-and-discussions)

## Code of Conduct

This project is committed to providing a welcoming and inclusive environment for all contributors. By participating, you agree to:

- Be respectful and considerate of others
- Use welcoming and inclusive language
- Be collaborative and open to constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## How Can I Contribute?

### Types of Contributions

We welcome various types of contributions:

- **Bug Reports**: Report bugs and issues you encounter
- **Feature Requests**: Suggest new features or improvements
- **Code Contributions**: Submit bug fixes, new features, or improvements
- **Documentation**: Improve or add documentation
- **Testing**: Help test the application and report issues
- **Examples**: Create example scripts or use cases

### Before You Start

1. Check existing issues and pull requests to avoid duplicates
2. Discuss major changes in an issue before implementing
3. Ensure your changes align with the project's goals

## Development Setup

### Prerequisites

- Python 3.7 or higher
- Git
- A webcam for testing
- Virtual environment (recommended)

### Local Development Setup

1. **Fork the repository**
   ```bash
   # Click "Fork" button on GitHub
   # Clone your fork
   git clone https://github.com/YOUR_USERNAME/Virtual-Mouse-Video-Controller.git
   cd Virtual-Mouse-Video-Controller
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a development branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

5. **Test the application**
   ```bash
   python VirtualMouse.py
   ```

## Code Style Guidelines

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use meaningful variable and function names
- Keep functions focused and under 50 lines when possible
- Add type hints where appropriate
- Use descriptive comments for complex logic

### Example of Good Code Style

```python
def calculate_hand_position(landmarks: List[Tuple[int, int, int]]) -> Tuple[int, int]:
    """
    Calculate the center position of the hand based on landmarks.
    
    Args:
        landmarks: List of (x, y, z) coordinates for hand landmarks
        
    Returns:
        Tuple of (center_x, center_y) coordinates
    """
    if not landmarks:
        return (0, 0)
    
    x_coords = [lm[0] for lm in landmarks]
    y_coords = [lm[1] for lm in landmarks]
    
    center_x = sum(x_coords) // len(x_coords)
    center_y = sum(y_coords) // len(y_coords)
    
    return (center_x, center_y)
```

### File Organization

- Keep related functionality in the same file
- Use clear file names that describe their purpose
- Organize imports: standard library, third-party, local
- Separate concerns between different modules

## Testing Guidelines

### Manual Testing

Before submitting changes:

1. **Test basic functionality**
   - Mouse cursor movement
   - Click detection
   - Video control gestures
   - Different lighting conditions

2. **Test edge cases**
   - Hand not detected
   - Poor lighting
   - Fast hand movements
   - Multiple gesture attempts

3. **Test on different systems**(IF POSSIBLE)
   - Windows, macOS, Linux
   - Different Python versions
   - Different webcam models

### Automated Testing

When possible, add unit tests for new functionality:

```python
import unittest
from HandTrackingModule import handDetector

class TestHandDetector(unittest.TestCase):
    def setUp(self):
        self.detector = handDetector()
    
    def test_finger_detection(self):
        # Test finger detection logic
        pass
    
    def test_gesture_recognition(self):
        # Test gesture recognition
        pass

if __name__ == '__main__':
    unittest.main()
```

## Pull Request Process

### Creating a Pull Request

1. **Ensure your code is ready**
   - All tests pass
   - Code follows style guidelines
   - Documentation is updated
   - No debugging code remains

2. **Write a clear description**
   - What changes were made
   - Why changes were needed
   - How to test the changes
   - Any breaking changes

3. **Submit the PR**
   - Use descriptive branch names
   - Reference related issues
   - Request reviews from maintainers

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement

## Testing
- [ ] Manual testing completed
- [ ] Unit tests added/updated
- [ ] Tested on different platforms

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No debugging code remains
```

## Reporting Issues

### Bug Report Template

When reporting bugs, please include:

```markdown
**Bug Description**
Clear description of the problem

**Steps to Reproduce**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Windows 10, macOS 12.0]
- Python Version: [e.g., 3.8.10]
- Package Versions: [from requirements.txt]
- Hardware: [e.g., webcam model]

**Additional Information**
Screenshots, error messages, logs
```

### Issue Guidelines

- Use descriptive titles
- Include relevant error messages
- Provide reproduction steps
- Mention your environment
- Check for duplicate issues first

## Feature Requests

### Feature Request Template

```markdown
**Feature Description**
Clear description of the requested feature

**Use Case**
Why this feature would be useful

**Proposed Implementation**
How you think it could be implemented

**Alternatives Considered**
Other approaches you've considered

**Additional Context**
Any other relevant information
```

## Questions and Discussions

### Getting Help

- Use GitHub Issues for questions
- Be specific about your problem
- Include relevant code snippets
- Mention what you've already tried

### Contributing to Discussions

- Be respectful and constructive
- Provide helpful feedback
- Share your experiences
- Help other contributors

## Recognition

Contributors will be recognized in:

- Project README
- Release notes
- Contributor statistics
- Special acknowledgments for significant contributions

## Getting Help

If you need help with contributing:

1. Check existing documentation
2. Search existing issues
3. Create a new issue with your question
4. Join community discussions

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

Thank you for contributing to Virtual Mouse with Video Control! Your contributions help make this project better for everyone.
