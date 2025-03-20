from pydantic import BaseModel
import json
import urllib.parse
import pandas as pd
import io
import logging
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger("chart_tool")


class ChartRequest(BaseModel):
    chart_type: str
    """The type of chart, such as bar, line, pie, etc."""

    title: str
    """The title of the chart"""

    data: str
    """Chart data in Markdown table format or JSON/CSV string"""

    description: str
    """A brief description of what the chart should show"""

    position: str
    """Where to place the chart in the report (e.g. {{chart_1}})"""


def parse_markdown_table(markdown_table: str) -> pd.DataFrame:
    """Parse a markdown table into a pandas DataFrame"""
    logger.debug("🔍 Parsing markdown table")
    lines = markdown_table.strip().split("\n")
    headers = [h.strip() for h in lines[0].strip("|").split("|")]

    # Skip the separator line
    data_rows = []
    for line in lines[2:]:  # Skip header and separator
        if line.strip():
            row = [cell.strip() for cell in line.strip("|").split("|")]
            data_rows.append(row)

    df = pd.DataFrame(data_rows, columns=headers)

    # Convert numeric columns
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

    return df


def generate_chart(chart_request: ChartRequest) -> str:
    """Generate a chart image based on the request and return a chart URL"""
    logger.info(
        f"📊 Generating {chart_request.chart_type} chart: {chart_request.title}"
    )

    try:
        # Parse the data
        data = chart_request.data.strip()
        df = None

        if data.startswith("|") and "\n" in data:
            df = parse_markdown_table(data)
        elif data.startswith("[") or data.startswith("{"):
            json_data = json.loads(data)
            if isinstance(json_data, dict):
                df = pd.DataFrame(
                    {
                        "Category": list(json_data.keys()),
                        "Value": list(json_data.values()),
                    }
                )
            else:
                df = pd.DataFrame(json_data)
        else:
            df = pd.read_csv(io.StringIO(data))

        if df is None:
            raise ValueError("Failed to parse chart data")

        # Get chart type
        chart_type = chart_request.chart_type.lower()
        logger.info(f"Processing chart type: {chart_type}")

        try:
            # Extract labels and data
            if len(df.columns) >= 2:
                labels = df[df.columns[0]].tolist()
                values = df[df.columns[1]].tolist()
                logger.info(
                    f"Using column '{df.columns[0]}' for labels and '{df.columns[1]}' for values"
                )
                logger.info(f"Labels: {labels[:5]}{'...' if len(labels) > 5 else ''}")
                logger.info(f"Values: {values[:5]}{'...' if len(values) > 5 else ''}")
            else:
                labels = [f"Item {i}" for i in range(len(df))]
                values = df[df.columns[0]].tolist()
                logger.info(
                    f"Using generated labels and column '{df.columns[0]}' for values"
                )
                logger.info(
                    f"Generated labels: {labels[:5]}{'...' if len(labels) > 5 else ''}"
                )
                logger.info(f"Values: {values[:5]}{'...' if len(values) > 5 else ''}")

            # Map chart type to QuickChart type
            qc_type = "bar"
            if "line" in chart_type:
                qc_type = "line"
            elif "pie" in chart_type:
                qc_type = "pie"
            elif "scatter" in chart_type:
                qc_type = "scatter"
            elif "doughnut" in chart_type:
                qc_type = "doughnut"
            logger.info(f"Mapped chart type to: {qc_type}")

            # Create chart configuration
            chart_config = {
                "type": qc_type,
                "data": {
                    "labels": labels,
                    "datasets": [
                        {
                            "label": chart_request.title,
                            "data": values,
                            "backgroundColor": [
                                "rgba(54, 162, 235, 0.5)",
                                "rgba(255, 99, 132, 0.5)",
                                "rgba(75, 192, 192, 0.5)",
                                "rgba(255, 206, 86, 0.5)",
                                "rgba(153, 102, 255, 0.5)",
                                "rgba(255, 159, 64, 0.5)",
                            ],
                            "borderColor": [
                                "rgba(54, 162, 235, 1)",
                                "rgba(255, 99, 132, 1)",
                                "rgba(75, 192, 192, 1)",
                                "rgba(255, 206, 86, 1)",
                                "rgba(153, 102, 255, 1)",
                                "rgba(255, 159, 64, 1)",
                            ],
                            "borderWidth": 2,
                        }
                    ],
                },
                "options": {
                    "responsive": True,
                    "maintainAspectRatio": True,
                    "plugins": {
                        "title": {
                            "display": True,
                            "text": chart_request.title,
                            "font": {"size": 18, "family": "Arial"},
                            "padding": 20,
                        },
                        "legend": {"display": True, "position": "bottom"},
                    },
                    "scales": {
                        "y": {
                            "beginAtZero": True,
                            "grid": {"display": True, "color": "rgba(0, 0, 0, 0.1)"},
                        },
                        "x": {"grid": {"display": False}},
                    },
                },
            }
            logger.info("Chart configuration created successfully")

            try:
                config_json = json.dumps(chart_config)
                encoded_config = urllib.parse.quote_plus(config_json)
                chart_url = f"https://quickchart.io/chart?c={encoded_config}"

                if len(chart_url) > 2000:
                    logger.warning(
                        "⚠️ Chart URL exceeds length limit, trying to compress data"
                    )

                logger.debug("✅ Chart URL generated successfully")
                return chart_url

            except Exception as e:
                logger.error(f"❌ Chart URL generation failed: {str(e)}")
                logger.debug(f"Config JSON: {config_json[:100]}...")
                return None

        except Exception as e:
            logger.error(f"❌ Chart generation failed: {str(e)}")
            return None

    except Exception as e:
        logger.error(f"❌ Chart generation failed: {str(e)}")
        return None
