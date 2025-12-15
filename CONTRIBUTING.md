# Contributing to AI Drama World Lab

Thank you for your interest in contributing to AI Drama World Lab! This document provides guidelines and instructions for contributing.

## How to Contribute

We welcome contributions in the following areas:
- Bug fixes
- New features
- Documentation improvements
- Performance optimizations
- Test coverage
- Examples and tutorials

## Getting Started

1. **Fork the repository**
```bash
git clone https://github.com/yourusername/ai-drama-world-lab.git
cd ai-drama-world-lab
```

2. **Set up the development environment**
   - Follow the instructions in [docs/SETUP.md](docs/SETUP.md)
   - Make sure all tests pass before making changes

3. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

## Development Workflow

### Backend Development

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Activate virtual environment**
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Make your changes**
   - Follow Python PEP 8 style guide
   - Add docstrings to functions and classes
   - Use type hints where appropriate

4. **Test your changes**
```bash
python -m pytest  # When tests are added
```

### Frontend Development

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Start development server**
```bash
npm run dev
```

3. **Make your changes**
   - Follow TypeScript and React best practices
   - Use existing components as style reference
   - Ensure responsive design

4. **Lint your code**
```bash
npm run lint
```

## Code Style Guidelines

### Python (Backend)
- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to all public functions/classes
- Use type hints for function parameters and returns
- Keep functions focused and small (< 50 lines when possible)

Example:
```python
def calculate_reward(self, world_state: Dict[str, Any]) -> float:
    """
    Calculate reward based on current state and world.
    
    Args:
        world_state: Current state of the world
        
    Returns:
        Calculated reward value
    """
    reward = 0.0
    # Implementation
    return reward
```

### TypeScript/React (Frontend)
- Use functional components with hooks
- Use TypeScript for all new code
- Follow React naming conventions
- Use CSS-in-JS or styled-jsx for styling
- Keep components focused (single responsibility)

Example:
```typescript
interface MyComponentProps {
  title: string;
  onAction: () => void;
}

export default function MyComponent({ title, onAction }: MyComponentProps) {
  return (
    <div>
      <h2>{title}</h2>
      <button onClick={onAction}>Action</button>
    </div>
  );
}
```

## Commit Guidelines

Follow conventional commit messages:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Examples:
```
feat: add multi-agent communication
fix: resolve memory leak in episode logger
docs: update API documentation
style: format code according to PEP 8
refactor: extract scene generation logic
test: add tests for agent behavior
chore: update dependencies
```

## Pull Request Process

1. **Update documentation**
   - Update README.md if needed
   - Add/update API documentation
   - Update CHANGELOG.md

2. **Test thoroughly**
   - Ensure all existing tests pass
   - Add tests for new features
   - Test in both development and production modes

3. **Create pull request**
   - Provide clear description of changes
   - Reference any related issues
   - Include screenshots for UI changes
   - List any breaking changes

4. **Code review**
   - Address review comments
   - Make requested changes
   - Re-request review when ready

5. **Merge**
   - Squash commits if requested
   - Delete feature branch after merge

## Adding New Features

### Adding a New Scene Type

1. Edit `backend/world/generator.py`
2. Add generation method (e.g., `_generate_space_station`)
3. Update prompt parsing logic
4. Add example prompts to frontend

### Adding a New Agent Behavior

1. Edit `backend/agents/embodied_agent.py`
2. Update `decide_action` method
3. Add new action types
4. Update reward calculation if needed

### Adding a New UI Component

1. Create component in `frontend/src/components/`
2. Add to main page layout
3. Update state management if needed
4. Add styles

## Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Integration Tests
```bash
# Start services
docker-compose up -d

# Run integration tests
# (to be added)
```

## Documentation

When adding features, update:
- README.md (if user-facing)
- docs/API.md (if API changes)
- docs/ARCHITECTURE.md (if architecture changes)
- docs/EXAMPLES.md (add usage examples)
- Code comments and docstrings

## Issue Reporting

When reporting bugs, include:
1. Description of the issue
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. Environment details (OS, Python/Node version, etc.)
6. Screenshots if applicable

Use issue templates when available.

## Feature Requests

When requesting features:
1. Describe the feature clearly
2. Explain use case and benefits
3. Provide examples if possible
4. Discuss implementation approach

## Community Guidelines

- Be respectful and constructive
- Help others in discussions
- Follow the code of conduct
- Give credit where due
- Have fun building!

## Questions?

If you have questions:
- Check existing documentation
- Search closed issues
- Open a new issue with the "question" label
- Join community discussions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to AI Drama World Lab! 🎭
