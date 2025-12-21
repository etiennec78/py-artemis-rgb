# Artemis RGB python client 💡

An asynchronous Python library for interacting with Artemis RGB software.

## Installation 🚀

```sh
pip install py-artemis-rgb
```

## Features 🌟

* Get Artemis profiles data 🎨
* Get Artemis profile categories data 🗂️
* Suspend Artemis profiles ⏸️
* Bring Artemis to the foreground (with an optional path) 🔔
* Restart Artemis (with arguments) 🔄
* Shutdown Artemis 🔌

## Usage ⚙️

Basic example of Artemis RGB client usage:

```python
import asyncio
from py_artemis_rgb import (
    Artemis,
    ArtemisConfig,
    ArtemisCannotConnectError,
    ArtemisUnknownType,
    ArtemisUnknownProfile,
)


async def main():
    # Configure the client
    config = ArtemisConfig(
        host="localhost",
        port=9696,
    )
    client = Artemis(config)

    try:
        # Get data about Artemis profiles
        profiles = await client.get_profiles()
        print("--- Profiles ---")
        for profile in profiles:
            print(
                f"The profile {profile.Id} named '{profile.Name}' from the '{profile.Category.Name}' category is {'suspended' if profile.IsSuspended else 'currently running'}."
            )

        # Get data about Artemis categories
        categories = await client.get_profile_categories()
        print("\n--- Categories ---")
        for category in categories:
            print(
                f"The category {category.Id} named '{category.Name}' is at the position n°{category.Order} and is {'suspended' if category.IsSuspended else 'currently running'}."
            )

        # Suspend all Artemis Profiles
        for profile in profiles:
            await client.suspend_profile(profile.Id, True)

        # Bring Artemis to the foreground and open the workshop
        await client.bring_to_foreground("workshop")

        # Restart Artemis without loading plugins
        await client.restart(["--no-plugins"])

        # Shutdown Artemis
        await client.shutdown()

    except ArtemisCannotConnectError:
        print(
            "Please check your config, and that the Artemis Web API plugin is enabled."
        )
    except ArtemisUnknownType:
        print("The API seems to have changed. Please open an issue on Github.")
    except ArtemisUnknownProfile:
        print("The given profile UUID does not match any profile in the server.")


if __name__ == "__main__":
    asyncio.run(main())
```
