# plantapop-core


## Architecture:

**Bounded Context:**

- `Chat` (Communication): This context is responsible for facilitating communication between users. Features may include direct messaging, notifications, and possibly scheduling in-person meetups for exchanges.

- `Discovery` (Search and Discovery): Manages product search and recommendation logic. Users can search for items based on various criteria like category, location, tags, and others. This context also handles the logic to display recommended products to the users.

- `Geolocation`: Handles users' location and calculates distances between them to display items from nearby sellers.

- `Labeling` (Product Cataloging): This context handles the classification and categorization of products. This includes the logic of assigning tags to products and creating and managing product categories and subcategories.

- `Plantory` (Product Management): Handles the lifecycle of a product - from its creation to its deletion. This includes adding new items, editing or deleting existing items.
