import requests
import json
import os

API_KEY = "sk_dd54f6018adf01f67f96c6e61f7adffa9b58c48b92a1c60a"

VOICEOVER = """
Thirty-five thousand feet above the mountains of Siberia. It is past midnight. The alarms are screaming.

And the captain of Aeroflot Flight 593 is not looking at his instruments.

He is screaming at his son to get out of the seat.

In the next four minutes, this aircraft will enter a spiral dive, stall twice, and descend below the minimum safe altitude over some of the most unforgiving terrain on Earth.

Seventy-five people will not survive.

And the official investigation will uncover a secret that shook the entire aviation world.

The evening of March 22nd, 1994. Moscow, Russia.

At Sheremetyevo International Airport, Aeroflot Flight 593 is preparing to depart for Hong Kong. The aircraft is an Airbus A310 — a modern, French-built widebody jet that Aeroflot had only recently begun flying as part of its post-Soviet modernization.

Sixty-three passengers settle into their seats. It is a long overnight flight. Most of them will try to sleep.

On the flight deck, Captain Yaroslav Kudrinsky takes his seat. He is 39 years old — an experienced aviator with nearly nine thousand hours in the air. He has flown Antonov freighters, Ilyushin jets, Yakovlev trainers. He has spent his entire career inside Soviet-built cockpits.

The A310 is different. Western. Digital. Sophisticated in ways that Soviet aircraft simply were not.

He has 907 hours on this type. Enough to feel comfortable. Enough, perhaps, to feel at ease.

Sitting beside him is First Officer Igor Piskaryov. And travelling as a passenger in the cabin — on a pilot's family discount — is an off-duty Aeroflot pilot named Vladimir Makarov.

Makarov is not the only one travelling on that discount tonight.

Captain Kudrinsky has brought his children on their first trip abroad.

His daughter, Yana. Twelve years old.
His son, Eldar. Fifteen.

They have never left Russia before. Their father is flying them to Hong Kong as a gift.

And somewhere over the dark expanse of Siberia, he will give them one more gift.

A gift that will kill everyone on board.
"""

def list_voices():
    response = requests.get(
        "https://api.elevenlabs.io/v1/voices",
        headers={"xi-api-key": API_KEY}
    )
    voices = response.json().get("voices", [])
    print("\nYour available voices:\n")
    for v in voices:
        print(f"  Name: {v['name']:<30} Voice ID: {v['voice_id']}")
    return voices

def generate_audio(voice_id, voice_name):
    print(f"\nGenerating audio with voice: {voice_name}...")
    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers={
            "xi-api-key": API_KEY,
            "Content-Type": "application/json"
        },
        json={
            "text": VOICEOVER.strip(),
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
    )

    if response.status_code == 200:
        output_file = "voiceover_hook_act1.mp3"
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"\nDone! Audio saved to: {os.path.abspath(output_file)}")
    else:
        print(f"\nError {response.status_code}: {response.text}")

if __name__ == "__main__":
    voices = list_voices()

    if not voices:
        print("No voices found on your account.")
    elif len(voices) == 1:
        generate_audio(voices[0]["voice_id"], voices[0]["name"])
    else:
        print("\nEnter the number of the voice you want to use:")
        for i, v in enumerate(voices):
            print(f"  [{i}] {v['name']}")
        choice = int(input("\nYour choice: "))
        generate_audio(voices[choice]["voice_id"], voices[choice]["name"])
