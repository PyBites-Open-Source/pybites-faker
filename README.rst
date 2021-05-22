## PyBites Faker

This package is an extension of the awesome `faker` package. It brings together a bunch of PyBites objects that can be randomly chosen. We started with our Bites and articles, but we can add more objects based on our content or personal preferences (think music for example).

### Setup

You can get the package with:

```
pip install pybites-faker
```

We included the code to get the initial data so it updates as we add more content.

We cache the data in a pickle file which is stored in `/tmp` by default. To store this file somewhere else set the `PYBITES_FAKER_DIR` environment variable.

Then you can get random PyBites objects like:
