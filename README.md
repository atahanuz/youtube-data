## -- This is not a complete program but some scripts being used for a research --

### Usage: get_videos_by_keyword

```python
results = search_youtube_videos('Felsefe', 3,truncate=False)
```
First argument: String to search in youtube
Second argument: Number of videos to get
Third argument: Truncate the results to 100 characters if set True

After obtaining the results, you can print or save them to a json file.
```python
#print_result(results)
#save_result(results,"results.json")
```

