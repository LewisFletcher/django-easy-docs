# Customizing

## Customizing the URL mapping
Easy Docs comes with two different URL mapping options. It can be done at the user level with regex patterns added directly to the model, or at the project level with a custom URL mapping setting. abstract

### User Level
To customize the URL mapping at the user level, you can add a regex pattern to the regex_pattern field on the Documentation model. This will allow you to customize the URL mapping for each individual document using a shared regex pattern. This can be helpful for keeping documentation consistent across different URLs which have a primary key (pk) in them, for example. To enable this feature, add the following to your settings.py file:

```python

USE_REGEX = True

```

### Project Level
To customize the URL mapping at the project level, you can add a custom URL mapping setting to your settings.py file. This will allow you to customize the URL mapping for all documents in the project. To enable this feature, add a 'URL MAP' to your settings.py file, as seen in the example below:

```python

URL_MAP = [
    (r'/products/\d+/', '/products/detail'),
    (r'/orders/\d+/edit/', '/orders/edit'),
    (r'/users/\d+/profile/', '/users/profile'),
]

```

The URL_MAP parameter should be a list of tuples, where each tuple consists of two elements:

    The first element is a regular expression pattern that matches the dynamic URLs you want to map.
    The second element is the replacement string that represents the generic URL pattern you want to map the dynamic URLs to.

For example, consider the URL_MAP seen above. This will map the following URLs:

    /products/123/ -> /products/detail
    /orders/456/edit/ -> /orders/edit
    /users/789/profile/ -> /users/profile

After the URL mapping is performed, Easy Docs will use the mapped generic URL pattern to look up the corresponding documentation in the database.

By customizing the URL mapping at the project level using the URL_MAPPING setting, you can define a centralized mapping that applies to all documents in your project. This can be useful for maintaining consistency and reducing duplication of URL patterns across multiple documents.

Note that if both the USE_REGEX and URL_MAPPING settings are defined, Easy Docs will first perform the project-level URL mapping using the URL_MAPPING setting, and then apply the user-level regex patterns defined in the regex_pattern field of individual documents.


## Customizing the template
If you would like to customize the template, you can do so by copying the `easy_docs` folder from the `templates` directory in the `easy_docs` app to your own templates directory. You can then make any changes you would like to the template.

## Customizing the CSS
If you would like to customize the CSS, you can do so by copying the `easy_docs` folder from the `static` directory in the `easy_docs` app to your own static directory. You can then make any changes you would like to the CSS.

## Future Customization
In the future, I plan to add the ability to customize the template and CSS via the settings.py file. If you would like to see this feature added, please open an issue on the [GitHub repo](https://github.com/LewisFletcher/django-easy-docs) and I will add it in a future release.