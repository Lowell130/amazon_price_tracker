import pytest
import sys
import os
from bs4 import BeautifulSoup

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.scraper import (
    get_asin_from_url, 
    clean_price, 
    parse_title, 
    parse_price_and_condition, 
    parse_image, 
    parse_rating,
    parse_details,
    parse_coupon
)

def test_get_asin_from_url():
    url_simple = "https://www.amazon.it/gp/product/B08N5N6V8H"
    assert get_asin_from_url(url_simple) == "B08N5N6V8H"

    url_dp = "https://www.amazon.it/dp/B08N5N6V8H/ref=sr_1_1"
    assert get_asin_from_url(url_dp) == "B08N5N6V8H"

    url_params = "https://www.amazon.it/dp/B08N5N6V8H?tag=foo"
    assert get_asin_from_url(url_params) == "B08N5N6V8H"
    
    # Test tracking param decoding (simulated)
    url_nested = "https://www.amazon.it/sspa/click?url=%2Fdp%2FB08N5N6V8H%2Fref%3Dfoo"
    assert get_asin_from_url(url_nested) == "B08N5N6V8H"

def test_clean_price():
    assert clean_price("19,99€") == 19.99
    assert clean_price("1.234,56 €") == 1234.56
    assert clean_price("1234,56") == 1234.56
    assert clean_price("1,234.56") == 1234.56 # American format fallback
    assert clean_price("Nuovo: 19,99") == 19.99
    assert clean_price(None) is None

def test_parse_title():
    html = '<div id="dp"><span id="productTitle"> Test Product </span></div>'
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("div", {"id": "dp"})
    assert parse_title(main) == "Test Product"

    html_none = '<div id="dp"></div>'
    soup_none = BeautifulSoup(html_none, "html.parser")
    main_none = soup_none.find("div", {"id": "dp"})
    assert parse_title(main_none) == "Titolo non disponibile"

def test_parse_price_new():
    html = '''
    <div id="dp">
        <div id="corePrice_feature_div">
            <span class="a-offscreen">19,99€</span>
        </div>
    </div>
    '''
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("div", {"id": "dp"})
    price, condition = parse_price_and_condition(main)
    assert price == 19.99
    assert condition == "Nuovo"

def test_parse_price_used():
    html = '''
    <div id="dp">
        <div id="usedBuySection">
            <span class="a-color-price">15,00€</span>
        </div>
    </div>
    '''
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("div", {"id": "dp"})
    price, condition = parse_price_and_condition(main)
    assert price == 15.00
    assert condition == "Usato"

def test_parse_out_of_stock():
    html = '''
    <div id="dp">
        <div id="outOfStock"></div>
    </div>
    '''
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("div", {"id": "dp"})
    price, condition = parse_price_and_condition(main)
    assert price is None
    assert condition == "Non disponibile"

def test_parse_image():
    html = '<div id="dp"><img id="landingImage" src="http://example.com/img.jpg"></div>'
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("div", {"id": "dp"})
    assert parse_image(main) == "http://example.com/img.jpg"

def test_parse_coupon():
    html = '<span><i class="newCouponBadge"></i><span>Applica coupon 2,00€</span></span>'
    soup = BeautifulSoup(html, "html.parser")
    coupon, value = parse_coupon(soup)
    assert coupon is True
    assert value == 2.00

    html_no_coupon = '<div></div>'
    soup_no = BeautifulSoup(html_no_coupon, "html.parser")
    coupon, value = parse_coupon(soup_no)
    assert coupon is False
    assert value is None
