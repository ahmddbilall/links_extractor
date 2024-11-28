import streamlit as st
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse

def categorize_links(base_url, links):
    internal_links = set()
    external_links = set()
    resource_links = set()

    for link in links:
        if not link:
            continue
        full_url = urljoin(base_url, link)
        parsed_url = urlparse(full_url)

        # Categorize links
        if base_url in full_url:
            internal_links.add(full_url)
        elif parsed_url.netloc and parsed_url.netloc != urlparse(base_url).netloc:
            external_links.add(full_url)
        elif full_url.endswith((".jpg", ".png", ".css", ".js", ".ico", ".svg")):
            resource_links.add(full_url)
    
    return internal_links, external_links, resource_links

# Streamlit UI
st.title("Website Link Extractor")
st.write("Enter a URL, and this app will extract and categorize all the links from that website.")

url = st.text_input("Enter Website URL:", placeholder="e.g., https://example.com")

if st.button("Extract Links") and url:
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        soup = BeautifulSoup(response.text, "html.parser")
        links = [a.get("href") for a in soup.find_all("a", href=True)]

        internal, external, resources = categorize_links(url, links)

        # Display categorized links
        st.subheader("Categorized Links")

        if internal:
            st.write("### Internal Links")
            for link in internal:
                st.write(f"- [Internal Link]({link})")

        if external:
            st.write("### External Links")
            for link in external:
                st.write(f"- [External Link]({link})")

        if resources:
            st.write("### Resource Links")
            for link in resources:
                st.write(f"- [Resource Link]({link})")

        if not (internal or external or resources):
            st.write("No links were found on the provided website.")

    except Exception as e:
        st.error(f"Error: {e}")
