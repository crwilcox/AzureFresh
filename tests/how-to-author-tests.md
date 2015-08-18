Authoring unit tests for python is rather straightforward.  At the end of this document you can see two implementations of a unit test.

AzureFresh has been developed using Python Tools for Visual Studio.  For information on authoring and running unit tests from PTVS visit https://github.com/microsoft/ptvs/wiki/Unit-Tests


Here is some sample code on how to implement the test case we have left incomplete in test_product_model.py

```python
import unittest
from app.models import Product
from unittest import mock
import httpretty

class Test_product_model(unittest.TestCase):
    def test_get_recommendations(self):
        items = Product(id=1).recommended_items
        self.assertIsNotNone(items)
        self.assertEqual(items[0].id, 2)

if __name__ == '__main__':
    unittest.main()
```

The above version will call the live service using the credentials in config.py.  In case you don't want your tests calling rest services, here is a more complete version using HTTPretty instead of making a call against the live REST Service.


```python
import unittest
from app.models import Product
from unittest import mock
import httpretty

class Test_product_model(unittest.TestCase):
    @httpretty.activate
    def test_get_recommendations(self):

        config.model_id = 'abcdabcd-1234-1234-1234-abcdabcdabcd'
        body = '''
			<feed xmlns:base="https://api.datamarket.azure.com/Data.ashx/amla/recommendations/v2/ItemRecommend" xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" xmlns:m="http://schemas.microsoft.com/ado/2007/08/dataservices/metadata" xmlns="http://www.w3.org/2005/Atom">
			    <title type="text" />
			    <subtitle type="text">Get Recommendation</subtitle>
			    <id>https://api.datamarket.azure.com/Data.ashx/amla/recommendations/v2/ItemRecommend?modelId='abcdabcd-1234-1234-1234-abcdabcdabcd'&amp;itemIds='1'&amp;numberOfResults=10&amp;includeMetadata=False&amp;apiVersion='1.0'</id>
			    <rights type="text" />
			    <updated>2015-08-18T19:04:25Z</updated>
			    <link rel="self" href="https://api.datamarket.azure.com/Data.ashx/amla/recommendations/v2/ItemRecommend?modelId='abcdabcd-1234-1234-1234-abcdabcdabcd'&amp;itemIds='1'&amp;numberOfResults=10&amp;includeMetadata=False&amp;apiVersion='1.0'" />
			    <entry>
			        <id>https://api.datamarket.azure.com/Data.ashx/amla/recommendations/v2/ItemRecommend?modelId='abcdabcd-1234-1234-1234-abcdabcdabcd'&amp;itemIds='1'&amp;numberOfResults=10&amp;includeMetadata=False&amp;apiVersion='1.0'&amp;$skip=0&amp;$top=1</id>
			        <title type="text">GetRecommendationEntity</title>
			        <updated>2015-08-18T19:04:25Z</updated>
			        <link rel="self" href="https://api.datamarket.azure.com/Data.ashx/amla/recommendations/v2/ItemRecommend?modelId='abcdabcd-1234-1234-1234-abcdabcdabcd'&amp;itemIds='1'&amp;numberOfResults=10&amp;includeMetadata=False&amp;apiVersion='1.0'&amp;$skip=0&amp;$top=1" />
			        <content type="application/xml">
			            <m:properties>
			                <d:Id m:type="Edm.String">2</d:Id>
			                <d:Name m:type="Edm.String">Honeycrisp Apple - Large</d:Name>
			                <d:Rating m:type="Edm.Double">10.4545454545455</d:Rating>
			                <d:Reasoning m:type="Edm.String">People who bought 'Granny Smith Apples - 3 lb Bag' also bought 'Honeycrisp Apple - Large'</d:Reasoning>
			            </m:properties>
			        </content>
			    </entry>
			</feed>'''

        url = 'https://api.datamarket.azure.com/amla/recommendations/v2/ItemRecommend?modelId="abcdabcd-1234-1234-1234-abcdabcdabcd"&itemIds="1"&numberOfResults=10&includeMetadata=False&apiVersion="1.0"'
        httpretty.register_uri(httpretty.GET, url, body=body)

        items = Product(id=1).recommended_items
        self.assertIsNotNone(items)
        self.assertEqual(items[0].id, 2)

if __name__ == '__main__':
    unittest.main()
```


