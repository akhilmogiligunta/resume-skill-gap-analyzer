RECOMMENDATION_MAP = {
    "Python": (
        "Strengthen Python programming, including functions, "
        "OOP, exception handling, modules, and common libraries."
    ),

    "Java": (
        "Strengthen Java programming, including OOP, "
        "collections, exception handling, and JDBC."
    ),

    "JavaScript": (
        "Learn modern JavaScript, including ES6+, "
        "DOM manipulation, asynchronous programming, and APIs."
    ),

    "TypeScript": (
        "Learn TypeScript fundamentals, including types, "
        "interfaces, generics, and TypeScript with React."
    ),

    "HTML": (
        "Strengthen HTML5, including semantic elements, "
        "forms, tables, and accessible page structure."
    ),

    "CSS": (
        "Strengthen CSS, including Flexbox, Grid, "
        "responsive design, and modern layouts."
    ),

    "React": (
        "Learn React components, props, state, hooks, "
        "routing, and API integration."
    ),

    "Node.js": (
        "Learn Node.js, including Express, REST APIs, "
        "middleware, and backend development."
    ),

    "Flask": (
        "Strengthen Flask by learning routes, templates, "
        "forms, APIs, and application structure."
    ),

    "Django": (
        "Learn Django models, views, URLs, templates, "
        "forms, and REST API development."
    ),

    "SQL": (
        "Strengthen SQL through SELECT queries, joins, "
        "subqueries, aggregation, and database design."
    ),

    "MySQL": (
        "Learn MySQL database design, queries, indexes, "
        "constraints, and transactions."
    ),

    "PostgreSQL": (
        "Learn PostgreSQL queries, indexing, transactions, "
        "and relational database design."
    ),

    "MongoDB": (
        "Learn MongoDB collections, documents, CRUD "
        "operations, indexes, and aggregation."
    ),

    "Git": (
        "Strengthen Git through branching, merging, "
        "commits, pull requests, and conflict resolution."
    ),

    "GitHub": (
        "Learn GitHub repositories, branches, pull requests, "
        "issues, and collaborative development."
    ),

    "Docker": (
        "Learn Docker images, containers, Dockerfiles, "
        "volumes, networking, and Docker Compose."
    ),

    "Kubernetes": (
        "Learn Kubernetes pods, deployments, services, "
        "configurations, and container orchestration."
    ),

    "AWS": (
        "Learn AWS fundamentals such as EC2, S3, IAM, "
        "Lambda, and basic cloud deployment."
    ),

    "Azure": (
        "Learn Azure fundamentals including virtual machines, "
        "storage, identity, and cloud deployment."
    ),

    "Machine Learning": (
        "Strengthen machine learning concepts including "
        "supervised learning, preprocessing, model evaluation, "
        "and feature engineering."
    ),

    "Deep Learning": (
        "Learn neural networks, backpropagation, CNNs, "
        "RNNs, and deep learning model evaluation."
    ),

    "NLP": (
        "Learn NLP preprocessing, tokenization, TF-IDF, "
        "embeddings, text classification, and language models."
    ),

    "TensorFlow": (
        "Learn TensorFlow model creation, training, "
        "evaluation, and neural network implementation."
    ),

    "PyTorch": (
        "Learn PyTorch tensors, datasets, neural networks, "
        "training loops, and model evaluation."
    ),

    "Scikit-learn": (
        "Strengthen Scikit-learn through preprocessing, "
        "classification, regression, clustering, and evaluation."
    ),

    "Pandas": (
        "Learn Pandas for data cleaning, DataFrames, "
        "filtering, grouping, merging, and analysis."
    ),

    "NumPy": (
        "Learn NumPy arrays, vectorized operations, "
        "indexing, broadcasting, and numerical computation."
    ),

    "Matplotlib": (
        "Learn Matplotlib for creating charts, plots, "
        "customized visualizations, and data exploration."
    ),

    "OpenCV": (
        "Learn OpenCV image processing, image transformations, "
        "feature detection, and computer vision basics."
    ),

    "Power BI": (
        "Learn Power BI data modeling, dashboards, "
        "visualizations, and basic DAX."
    ),

    "Google Cloud": (
        "Learn Google Cloud fundamentals including compute, "
        "storage, IAM, and basic cloud deployment."
    ),

    "Redis": (
        "Learn Redis data structures, caching, expiration, "
        "and basic in-memory database usage."
    )
}


def generate_recommendations(missing_skills):
    """
    Generate skill-specific recommendations
    for skills missing from the resume.
    """

    if not missing_skills:
        return [
            "Your resume covers all recognized required skills."
        ]

    recommendations = []

    for skill in missing_skills:

        recommendation = RECOMMENDATION_MAP.get(
            skill,
            (
                f"Consider learning or strengthening "
                f"{skill}."
            )
        )

        recommendations.append(
            f"{skill}: {recommendation}"
        )

    return recommendations