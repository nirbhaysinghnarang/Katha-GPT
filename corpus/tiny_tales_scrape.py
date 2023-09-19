import requests
from bs4 import BeautifulSoup
import re

# Define the URL of the main page containing the links to stories
main_url = "https://microfables.blogspot.com/2020/11/tiny-tales-from-mahabharata.html"

# Send an HTTP GET request to the main page
main_response = requests.get(main_url)

# Define the regex pattern to match the desired links
link_pattern = re.compile(r"https://microfables\.blogspot\.com/2020/11/.*")

# Define a regex pattern to extract the title from the story content
title_pattern = re.compile(r"^\d+\.\s+(.*)$")

# Check if the request was successful
if main_response.status_code == 200:
    # Parse the HTML content of the main page using BeautifulSoup
    main_soup = BeautifulSoup(main_response.content, "html.parser")

    # Find and extract the links to individual story pages using the regex pattern
    story_links = main_soup.find_all("a", href=link_pattern)

    # Loop through each story link and scrape the content from the individual story page
    for link in story_links:
        story_url = link["href"]
        story_response = requests.get(story_url)
        
        # Check if the request for the individual story page was successful
        if story_response.status_code == 200:
            # Parse the HTML content of the individual story page using BeautifulSoup
            story_soup = BeautifulSoup(story_response.content, "html.parser")
            
            # Find and extract the story content
            story_content = story_soup.find("div", class_="post-body")
            
            # Extract the title from the story content
            story_text = story_content.get_text()
            title = story_soup.find("h3").text
            
            # Create a new file with the title and write the story content to it
            with open(f"{title}.txt", "w", encoding="utf-8") as story_file:
                story_file.write(story_text)
                
            print(f"Saved story: {title}")
        else:
            print(f"Failed to retrieve the story page: {story_url}")

else:
    print("Failed to retrieve the main page.")
