import { render, screen } from '@testing-library/react';
// Importing the component you want to test (in this case, the main App component
import App from '../App.js';

/*
test() defines a single test case.

The first argument is the name of the test (for readability in test reports).

The second argument is a callback function containing the test logic.
*/

test('renders learn react link', () => {
  render(<App />);
  // Uses the screen.getByText() method to find an element that contains
  //  text matching the regex /learn react/i 
  // /i — Case-Insensitive Flag
  const linkElement = screen.getByText(/learn react/i);
  
  // expect() is a Jest global function used to make assertions.
  // .toBeInTheDocument() is a custom matcher from @testing-library/jest-dom
  //  that checks whether the element exists in the DOM.
  expect(linkElement).toBeInTheDocument();

});


/*
It checks that when the App component is rendered, an element 
with the text "learn react" (case-insensitive) is present in the DOM.
*/