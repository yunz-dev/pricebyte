const Woolworths = require('woolies'); // Require the API in your document

async function myAsyncFunction() {
  try {
    const result = await Woolworths.Search("a");
    console.log(result);
  } catch (error) {
    console.error('Error:', error);
  }
}

myAsyncFunction();
