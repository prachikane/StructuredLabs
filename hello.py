from preswald import text, plotly, connect, get_df, slider, table, query
import pandas as pd
import plotly.express as px

# App Title
text("# Handwriting Speed & Personality Insights")
text("Explore how writing speed relates to Big Five personality traits using interactive controls.")

# Connect to Data
connect()
df_raw = get_df("handwriting_personality")

# Select and clean relevant columns
columns_to_use = [
    "Writing_Speed_wpm", "Openness", "Conscientiousness",
    "Extraversion", "Agreeableness", "Neuroticism", "Gender", "Age"
]

df = df_raw[columns_to_use].copy()

# Convert numerics and drop missing values
for col in ["Writing_Speed_wpm", "Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism", "Age"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
df.dropna(inplace=True)

#Data Preview
#text("## Dataset Preview")
#table(df.head(), title="Cleaned Personality Data Sample")

# SQL Query for average features based on average age
sql = "SELECT Gender, AVG(Writing_Speed_wpm) AS avg_speed, AVG(Openness) AS avg_openness, AVG(Conscientiousness) AS avg_conscientiousness, AVG(Extraversion) AS avg_extraversion, AVG(Agreeableness) AS avg_agreeableness, AVG(Neuroticism) AS avg_neuroticism, AVG(Age) AS avg_age FROM handwriting_personality GROUP BY Gender"
sql_result = query(sql, "handwriting_personality")

#table(sql_result, title="SQL Query Results")

# Create Visualization
text("## Average Writing Speed and Personality Traits by Gender")

# Reshape for grouped bar chart
melted = sql_result.melt(id_vars="Gender", 
                         var_name="Trait", 
                         value_name="Average")

# Clean trait labels for display
trait_labels = {
    "avg_speed": "Writing Speed (wpm)",
    "avg_openness": "Openness",
    "avg_conscientiousness": "Conscientiousness",
    "avg_extraversion": "Extraversion",
    "avg_agreeableness": "Agreeableness",
    "avg_neuroticism": "Neuroticism"
}
melted["Trait"] = melted["Trait"].map(trait_labels)

# Create grouped bar chart
fig1 = px.bar(
    melted,
    x="Trait",
    y="Average",
    color="Gender",
    barmode="group",
    title="Average Writing Speed and Personality Traits by Gender",
    labels={"Average": "Average Score", "Trait": "Trait"}
)
fig1.update_layout(template="plotly_white")

plotly(fig1)


# Visualization: Personality vs Writing Speed
text("## Personality Traits vs Writing Speed")
fig2 = px.scatter(
    df,
    x="Writing_Speed_wpm",
    y="Openness",
    color="Gender",
    size="Age",
    render_mode="svg",
    hover_data=["Extraversion", "Conscientiousness", "Agreeableness", "Neuroticism"],
    title="Openness vs Writing Speed Colored by Gender"
)
plotly(fig2)

# Distribution of Traits
text("## Distribution of Big Five Traits")
for trait in ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]: 
    hist_fig = px.histogram(df, x=trait, color="Gender", title=f"{trait} Distribution by Gender") 
    plotly(hist_fig)

# Overview & Filtering
text("## Filter by Age and Writing Speed")
min_age = slider("Minimum Age", min_val=int(df["Age"].min()), max_val=int(df["Age"].max()), default=25)
min_speed = slider("Minimum Writing Speed (wpm)", min_val=int(df["Writing_Speed_wpm"].min()), max_val=int(df["Writing_Speed_wpm"].max()), default=20)
filtered_df = df[(df["Age"] >= min_age) & (df["Writing_Speed_wpm"] >= min_speed)]

table(filtered_df, title=f"People with Age ≥ {min_age} and Speed ≥ {min_speed} wpm")
