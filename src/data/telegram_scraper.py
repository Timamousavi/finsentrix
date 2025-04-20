from telethon import TelegramClient, events
from telethon.tl.types import Channel
import pandas as pd
from datetime import datetime
import asyncio
import logging
from typing import List, Dict, Optional
import json

class TelegramScraper:
    def __init__(self, api_id: int, api_hash: str, session_name: str = 'telegram_scraper'):
        """
        Initialize the Telegram scraper with API credentials.
        
        Args:
            api_id (int): Telegram API ID
            api_hash (str): Telegram API Hash
            session_name (str): Session name for the client
        """
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_name = session_name
        self.client = None
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='telegram_scraper.log'
        )
        self.logger = logging.getLogger(__name__)

    async def connect(self):
        """Connect to Telegram API."""
        try:
            self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)
            await self.client.start()
            self.logger.info("Successfully connected to Telegram")
        except Exception as e:
            self.logger.error(f"Failed to connect to Telegram: {str(e)}")
            raise

    async def get_channel_messages(self, channel_username: str, limit: int = 100) -> List[Dict]:
        """
        Get messages from a Telegram channel.
        
        Args:
            channel_username (str): Channel username or ID
            limit (int): Maximum number of messages to fetch
            
        Returns:
            List[Dict]: List of messages with metadata
        """
        messages = []
        try:
            channel = await self.client.get_entity(channel_username)
            async for message in self.client.iter_messages(channel, limit=limit):
                if message.text:  # Only process text messages
                    message_data = {
                        'text': message.text,
                        'date': message.date.isoformat(),
                        'views': message.views,
                        'forwards': message.forwards,
                        'channel': channel_username,
                        'message_id': message.id
                    }
                    messages.append(message_data)
            
            self.logger.info(f"Successfully fetched {len(messages)} messages from {channel_username}")
        except Exception as e:
            self.logger.error(f"Error fetching messages from {channel_username}: {str(e)}")
            
        return messages

    async def monitor_channel(self, channel_username: str, callback):
        """
        Monitor a channel for new messages and call the callback function.
        
        Args:
            channel_username (str): Channel username or ID
            callback: Function to call when new messages are received
        """
        try:
            channel = await self.client.get_entity(channel_username)
            
            @self.client.on(events.NewMessage(chats=channel))
            async def handler(event):
                message_data = {
                    'text': event.message.text,
                    'date': event.message.date.isoformat(),
                    'views': event.message.views,
                    'forwards': event.message.forwards,
                    'channel': channel_username,
                    'message_id': event.message.id
                }
                await callback(message_data)
                
            self.logger.info(f"Started monitoring {channel_username}")
            await self.client.run_until_disconnected()
            
        except Exception as e:
            self.logger.error(f"Error monitoring {channel_username}: {str(e)}")

    def save_to_csv(self, data: List[Dict], filename: str):
        """
        Save scraped data to CSV file.
        
        Args:
            data (List[Dict]): Data to save
            filename (str): Output filename
        """
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8')
        self.logger.info(f"Saved {len(data)} messages to {filename}")

    def save_to_json(self, data: List[Dict], filename: str):
        """
        Save scraped data to JSON file.
        
        Args:
            data (List[Dict]): Data to save
            filename (str): Output filename
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        self.logger.info(f"Saved {len(data)} messages to {filename}")

    async def close(self):
        """Close the Telegram client connection."""
        if self.client:
            await self.client.disconnect()
            self.logger.info("Disconnected from Telegram")

# Example usage:
async def main():
    # Initialize scraper with your API credentials
    scraper = TelegramScraper(
        api_id=YOUR_API_ID,  # Replace with your API ID
        api_hash='YOUR_API_HASH'  # Replace with your API Hash
    )
    
    try:
        # Connect to Telegram
        await scraper.connect()
        
        # List of financial channels to scrape
        channels = [
            'tse_ir',  # Tehran Stock Exchange
            'iran_stock',  # Example channel
            'financial_news_ir'  # Example channel
        ]
        
        # Scrape messages from each channel
        for channel in channels:
            messages = await scraper.get_channel_messages(channel, limit=100)
            scraper.save_to_csv(messages, f"data/raw/telegram_{channel}.csv")
            
    finally:
        # Always close the connection
        await scraper.close()

if __name__ == "__main__":
    asyncio.run(main()) 