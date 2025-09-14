from setuptools import setup, find_packages

setup(
    name="instantly",
    version="0.1.0",
    description="A unified interface for Hugging Face Inference Providers with OpenAI API compatibility",
    author="Instantly Team",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "huggingface_hub>=0.19.0",
        "pillow>=10.0.0",
        "requests>=2.31.0",
        "google-generativeai>=0.3.0",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)