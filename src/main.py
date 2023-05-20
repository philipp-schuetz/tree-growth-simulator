from modules.app import App

app = App()

if __name__ == "__main__":
    app.run()


# TODO recalculate light levels only when needed, does tree need light every step?

# TODO add process logging
# TODO enable the user to get images with and without leafs at the same time
# leaf generation
# from bottom to top?
# minimum lightlevel for leafes
# place next to wood, configure direct or diagonal in config file