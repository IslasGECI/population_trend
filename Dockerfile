FROM python:3.10
WORKDIR /workdir
COPY . .
RUN pip install --upgrade pip && pip install \
    black \
    flake8 \
    geci-test-tools \
    mutmut \
    mypy \
    pylint \
    pytest \
    pytest-cov \
    pytest-mpl
