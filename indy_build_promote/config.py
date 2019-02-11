from os.path import join
from os import getcwd
from ruamel.yaml import YAML

# group: pnc-builds
# target-repo: consolidated-builds
# project: newcastle-stage
# token: "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ5emxOa0tBUmZlMUVzcHZJbU9rdkVTeUttVGl6N05MTWp2Z3lSSGJEZHVBIn0.eyJqdGkiOiJkOWExZjYwYS1mZWRjLTQyYTYtYjVmOC04OGE1N2QzZTM4OTEiLCJleHAiOjE1NDk3NDMzNDMsIm5iZiI6MCwiaWF0IjoxNTQ5NjU2OTUzLCJpc3MiOiJodHRwczovL3NlY3VyZS1zc28tbmV3Y2FzdGxlLWRldmVsLmNsb3VkLnBhYXMudXBzaGlmdC5yZWRoYXQuY29tL2F1dGgvcmVhbG1zL3BuY3JlZGhhdCIsImF1ZCI6WyJwbmN3ZWIiLCJwbmNpbmR5IiwiYWNjb3VudCIsInBuY3Jlc3QiXSwic3ViIjoiODQ4ZGNjNjMtZDM5Yy00OGQ5LWI5ZTYtMThhMjFiNTkxNjNlIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoicG5jaW5keXVpIiwibm9uY2UiOiJmZjRkMTZjNi0zNTZhLTQwMDItODBjNy03NWVjMmQ5YTkyNjEiLCJhdXRoX3RpbWUiOjE1NDk2NTY5NDMsInNlc3Npb25fc3RhdGUiOiIyODhhYjMyZS1iMzA2LTQxZTEtYTg3Yy1iNzUyNTQxYjE4OGIiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbInVzZXIiXX0sInJlc291cmNlX2FjY2VzcyI6eyJwbmN3ZWIiOnsicm9sZXMiOlsidXNlciJdfSwicG5jaW5keXVpIjp7InJvbGVzIjpbInBuY2luZHlhZG1pbiIsInBuY2luZHl1c2VyIl19LCJwbmNpbmR5Ijp7InJvbGVzIjpbInBuY2luZHlhZG1pbiIsInBvd2VyLXVzZXIiLCJwbmNpbmR5dXNlciJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19LCJwbmNyZXN0Ijp7InJvbGVzIjpbInVzZXIiXX19LCJzY29wZSI6Im9wZW5pZCIsInByZWZlcnJlZF91c2VybmFtZSI6ImpjYXNleSIsImVtYWlsIjoiamNhc2V5QHJlZGhhdC5jb20ifQ.RySHtQB1PCme9DilGmt0Fg-mPYveOiMqp0-IObVXhRFqFPjf41kJJKuaW9b_UGM2c9EtfgpKRy5Q3Ag9biuUf6ffIV2_MRqIW6Bn5mii9RcD87lrfHumFscHj34a-fN5p5ZdOqhaA41YJ5baBq28rxcBphO0zRO8EGR6F0GxM8M30j83br2L4PDIJXerkJrLQX1M6SEpsvzYKKpc5-5CSvM4U6H9XqbZgmSXzUotkEEG9blQteROKhfJRocQ7fqjkTjgmK_z-3ZhFyGZ0f-95lSnA4gI1v7PkZhlr9mPJAB_8Rxfd6cEuFwIKla2u3EMb4Q7GNWAv9P5qbEjlpjLnA"
# url: http://indy-stage.psi.redhat.com

GROUP='group'
TARGET_REPO = 'target-repo'
PROJECT = 'project'
TOKEN = 'token'
URL = 'url'

DEFAULT_CONFIG_FILE = join(getcwd(), 'config.yml')

def load(config_file=DEFAULT_CONFIG_FILE):
	with open(config_file) as f:
		y = YAML(typ='safe')
		return Config( y.load(f) )

class Config:
	def __init__(self, data):
		self.group = data.get(GROUP)
		self.target_repo = data.get(TARGET_REPO)
		self.project = data.get(PROJECT)
		self.token = data.get(TOKEN)
		self.url = data.get(URL)


