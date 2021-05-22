class PyBitesData:
    bites = []
    articles = []

    def __str__(self):
        public_attrs = (name for name in dir(self)
                        if not name.startswith('_'))
        out = []
        for attr in public_attrs:
            items = getattr(self, attr)
            out.append(
                f"{attr.title()} => {len(items)} objects\n")
        return "".join(out)
