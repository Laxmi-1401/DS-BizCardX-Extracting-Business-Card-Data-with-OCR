{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "gpuType": "T4",
      "authorship_tag": "ABX9TyM10MAAtp3ZINFFoBYClK1Q",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    },
    "accelerator": "GPU"
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/drive/13kpBSjzbjlrUJ3Tm3kfmZOyaFWy9rTJO#\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "ddPdmT_Az-YE"
      },
      "outputs": [],
      "source": [
        "!pip install streamlit"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install pyngrok"
      ],
      "metadata": {
        "id": "CMJF_hJG0MHt"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "!npm install localtunnel"
      ],
      "metadata": {
        "id": "SHnMQrH40Tri"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install easyocr"
      ],
      "metadata": {
        "id": "ltyVXHEx0ZO_"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install streamlit_option_menu"
      ],
      "metadata": {
        "id": "1JKSI2id0tx7"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "%load_ext sql"
      ],
      "metadata": {
        "id": "U_a4KxKz1Se6"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# INITIALIZING THE EasyOCR READER\n",
        "#reader = easyocr.Reader(['en'])"
      ],
      "metadata": {
        "id": "e90SVrSO_J7r"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "#Writing in streamlit\n",
        "\n",
        "%%writefile app.py\n",
        "import pandas as pd\n",
        "import streamlit as st\n",
        "from streamlit_option_menu import option_menu\n",
        "import easyocr\n",
        "from PIL import Image\n",
        "import cv2\n",
        "import os\n",
        "import matplotlib.pyplot as plt\n",
        "import re\n",
        "import numpy as np\n",
        "import io\n",
        "\n",
        "import sqlite3\n",
        "con = sqlite3.connect(\"bizcard.db\")\n",
        "cur = con.cursor()\n",
        "\n",
        "#tittle\n",
        "#background_color = '#f0f0f0'  # Specify your desired background color in hex format\n",
        "\n",
        "\n",
        "st.markdown(f\"\"\" <style>.stApp {{\n",
        "                        background:url(\"https://click4vector.com/public/uploads/preview/abstract-wave-vector-background-hd-wallpaper-image-11641898933uccrtv4yqv.jpg\");\n",
        "                        background-size: cover}}\n",
        "                     </style>\"\"\", unsafe_allow_html=True)\n",
        "\n",
        "st.markdown(\"<h1 style='text-align: center; color: RED ;'>BizCardX: Extracting Business Card Data with OCR </h1>\", unsafe_allow_html=True)\n",
        "\n",
        "#option menu\n",
        "\n",
        "selected = option_menu(\n",
        "    menu_title=None,\n",
        "    options=[\"Image\", \"Contact\"],\n",
        "    icons=[\"image\", \"at\"],\n",
        "    default_index=0,\n",
        "    orientation=\"horizontal\"\n",
        ")\n",
        "\n",
        "# extract the data\n",
        "def extracted_text(picture):\n",
        "    ext_dic = {'Name': [], 'Designation': [], 'Company name': [], 'Contact': [], 'Email': [], 'Website': [],\n",
        "               'Address': [], 'Pincode': []}\n",
        "\n",
        "    ext_dic['Name'].append(result[0])\n",
        "    ext_dic['Designation'].append(result[1])\n",
        "\n",
        "    for m in range(2, len(result)):\n",
        "        if result[m].startswith('+') or (result[m].replace('-', '').isdigit() and '-' in result[m]):\n",
        "            ext_dic['Contact'].append(result[m])\n",
        "\n",
        "        elif '@' in result[m] and '.com' in result[m]:\n",
        "            small = result[m].lower()\n",
        "            ext_dic['Email'].append(small)\n",
        "\n",
        "        elif 'www' in result[m] or 'WWW' in result[m] or 'wwW' in result[m]:\n",
        "            small = result[m].lower()\n",
        "            ext_dic['Website'].append(small)\n",
        "\n",
        "        elif 'TamilNadu' in result[m] or 'Tamil Nadu' in result[m] or result[m].isdigit():\n",
        "            ext_dic['Pincode'].append(result[m])\n",
        "\n",
        "        elif re.match(r'^[A-Za-z]', result[m]):\n",
        "            ext_dic['Company name'].append(result[m])\n",
        "\n",
        "        else:\n",
        "            removed_colon = re.sub(r'[,;]', '', result[m])\n",
        "            ext_dic['Address'].append(removed_colon)\n",
        "\n",
        "    for key, value in ext_dic.items():\n",
        "        if len(value) > 0:\n",
        "            concatenated_string = ' '.join(value)\n",
        "            ext_dic[key] = [concatenated_string]\n",
        "        else:\n",
        "            value = 'NA'\n",
        "            ext_dic[key] = [value]\n",
        "\n",
        "    return ext_dic\n",
        "\n",
        "\n",
        "if selected == \"Image\":\n",
        "    image = st.file_uploader(label=\"Upload the image\", type=['png', 'jpg', 'jpeg'], label_visibility=\"hidden\")\n",
        "\n",
        "\n",
        "    @st.cache_data\n",
        "    def load_image():\n",
        "        reader = easyocr.Reader(['en'], model_storage_directory=\".\")\n",
        "        return reader\n",
        "\n",
        "\n",
        "    reader_1 = load_image()\n",
        "    if image is not None:\n",
        "        input_image = Image.open(image)\n",
        "        # Setting Image size\n",
        "        st.image(input_image, width=350, caption='Uploaded Image')\n",
        "        st.markdown(\n",
        "            f'<style>.css-1aumxhk img {{ max-width: 300px; }}</style>',\n",
        "            unsafe_allow_html=True\n",
        "        )\n",
        "\n",
        "        result = reader_1.readtext(np.array(input_image), detail=0)\n",
        "        # creating dataframe\n",
        "        ext_text = extracted_text(result)\n",
        "        df = pd.DataFrame(ext_text)\n",
        "        st.dataframe(df)\n",
        "\n",
        "        # Converting image into bytes\n",
        "        image_bytes = io.BytesIO()\n",
        "        input_image.save(image_bytes, format='PNG')\n",
        "        image_data = image_bytes.getvalue()\n",
        "\n",
        "        # Creating dictionary\n",
        "        data = {\"Image\": [image_data]}\n",
        "        df_1 = pd.DataFrame(data)\n",
        "        concat_df = pd.concat([df, df_1], axis=1)\n",
        "\n",
        "        # Database\n",
        "        col1, col2, col3 = st.columns([1, 6, 1])\n",
        "        with col2:\n",
        "            selected = option_menu(\n",
        "                menu_title=None,\n",
        "                options=[\"Preview\", \"Delete\"],\n",
        "                icons=['file-earmark', 'trash'],\n",
        "                default_index=0,\n",
        "                orientation=\"horizontal\"\n",
        "            )\n",
        "\n",
        "            ext_text = extracted_text(result)\n",
        "            df = pd.DataFrame(ext_text)\n",
        "        if selected == \"Preview\":\n",
        "            col_1, col_2 = st.columns([4, 4])\n",
        "            with col_1:\n",
        "                modified_n = st.text_input('Name', ext_text[\"Name\"][0])\n",
        "                modified_d = st.text_input('Designation', ext_text[\"Designation\"][0])\n",
        "                modified_c = st.text_input('Company name', ext_text[\"Company name\"][0])\n",
        "                modified_con = st.text_input('Mobile', ext_text[\"Contact\"][0])\n",
        "                concat_df[\"Name\"], concat_df[\"Designation\"], concat_df[\"Company name\"], concat_df[\n",
        "                    \"Contact\"] = modified_n, modified_d, modified_c, modified_con\n",
        "            with col_2:\n",
        "                modified_m = st.text_input('Email', ext_text[\"Email\"][0])\n",
        "                modified_w = st.text_input('Website', ext_text[\"Website\"][0])\n",
        "                modified_a = st.text_input('Address', ext_text[\"Address\"][0][1])\n",
        "                modified_p = st.text_input('Pincode', ext_text[\"Pincode\"][0])\n",
        "                concat_df[\"Email\"], concat_df[\"Website\"], concat_df[\"Address\"], concat_df[\n",
        "                    \"Pincode\"] = modified_m, modified_w, modified_a, modified_p\n",
        "\n",
        "            col3, col4 = st.columns([4, 4])\n",
        "            with col3:\n",
        "                Preview = st.button(\"Preview modified text\")\n",
        "            with col4:\n",
        "                Upload = st.button(\"Upload\")\n",
        "            if Preview:\n",
        "                filtered_df = concat_df[\n",
        "                    ['Name', 'Designation', 'Company name', 'Contact', 'Email', 'Website', 'Address', 'Pincode']]\n",
        "                st.dataframe(filtered_df)\n",
        "            else:\n",
        "                pass\n",
        "\n",
        "            if Upload:\n",
        "                with st.spinner(\"In progress\"):\n",
        "                    cur.execute(\n",
        "                        \"CREATE TABLE IF NOT EXISTS BUSINESS_CARD(NAME VARCHAR(50), DESIGNATION VARCHAR(100), \"\n",
        "                        \"COMPANY_NAME VARCHAR(100), CONTACT VARCHAR(35), EMAIL VARCHAR(100), WEBSITE VARCHAR(\"\n",
        "                        \"100), ADDRESS TEXT, PINCODE VARCHAR(100))\")\n",
        "                    con.commit()\n",
        "                    A = \"INSERT INTO BUSINESS_CARD(NAME, DESIGNATION, COMPANY_NAME, CONTACT, EMAIL, WEBSITE, ADDRESS, \" \\\n",
        "                        \"PINCODE) VALUES (?, ?, ?, ?, ?, ?, ?, ?)\"\n",
        "                    for index, i in concat_df.iterrows():\n",
        "                        result_table = (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])\n",
        "                        cur.execute(A, result_table)\n",
        "                        con.commit()\n",
        "                        st.success('SUCCESSFULLY UPLOADED', icon=\"✅\")\n",
        "        else:\n",
        "            col1, col2 = st.columns([4, 4])\n",
        "            with col1:\n",
        "                cur.execute(\"SELECT NAME FROM BUSINESS_CARD\")\n",
        "                Y = cur.fetchall()\n",
        "                names = [\"Select\"]\n",
        "                for i in Y:\n",
        "                    names.append(i[0])\n",
        "                name_selected = st.selectbox(\"Select the name to delete\", options=names)\n",
        "                # st.write(name_selected)\n",
        "            with col2:\n",
        "                cur.execute(f\"SELECT DESIGNATION FROM BUSINESS_CARD WHERE NAME = '{name_selected}'\")\n",
        "                Z = cur.fetchall()\n",
        "                designation = [\"Select\"]\n",
        "                for j in Z:\n",
        "                    designation.append(j[0])\n",
        "                designation_selected = st.selectbox(\"Select the designation of the chosen name\", options=designation)\n",
        "\n",
        "            st.markdown(\" \")\n",
        "\n",
        "            col_a, col_b, col_c = st.columns([5, 3, 3])\n",
        "            with col_b:\n",
        "                remove = st.button(\"Clik here to delete\")\n",
        "            if name_selected and designation_selected and remove:\n",
        "                cur.execute(\n",
        "                    f\"DELETE FROM BUSINESS_CARD WHERE NAME = '{name_selected}' AND DESIGNATION = '{designation_selected}'\")\n",
        "                con.commit()\n",
        "                if remove:\n",
        "                    st.warning('DELETED', icon=\"⚠️\")\n",
        "\n",
        "    else:\n",
        "        st.write(\"Upload an image\")\n",
        "if selected == \"Contact\":\n",
        "    name = \"Anupriya\"\n",
        "    mail = (f'{\"Mail :\"}  {\"lakshmimamdapure@gmail.com\"}')\n",
        "    description = \"An Aspiring DATA-SCIENTIST..!\"\n",
        "    social_media = {\n",
        "        \"GITHUB\": \"https://github.com/Laxmi-1401\",\n",
        "        \"LINKEDIN\": \"https://www.linkedin.com/in/laxmi-mamdapure-612954167/\"}\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "    col1, col2 = st.columns(2)\n",
        "    #col3.image(Image.open(\"/content/dark-background-empty-room-with-plants-floor_41470-1526.avif\"), width=250)\n",
        "    with col2:\n",
        "        st.title('BizCardX: Extracting Business Card Data with OCR')\n",
        "        st.write(\n",
        "            \"BizCardX is to automate and simplify the process of capturing and managing contact information from business cards, saving users time and effort. It is particularly useful for professionals who frequently attend networking events, conferences, and meetings where they receive numerous business cards that need to be converted into digital contacts.\")\n",
        "        st.write(\"---\")\n",
        "        st.subheader(mail)\n",
        "    st.write(\"#\")\n",
        "    cols = st.columns(len(social_media))\n",
        "    for index, (platform, link) in enumerate(social_media.items()):\n",
        "        cols[index].write(f\"[{platform}]({link})\")\n"
      ],
      "metadata": {
        "id": "VJ7A9BALFAoO",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "32f12c10-1c2a-4155-cdb6-647957e7bafd"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Overwriting app.py\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#streamlit run\n",
        "\n",
        "!streamlit run /content/app.py &>/content/logs.txt & npx localtunnel --port 8501 & curl ipv4.icanhazip.com"
      ],
      "metadata": {
        "id": "rhsyrPh_n5ku"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "import sqlite3\n",
        "con = sqlite3.connect(\"bizcard.db\")\n",
        "cur = con.cursor()\n",
        "cur.execute(\"select * from BUSINESS_CARD\")\n",
        "view_table=cur.fetchall()\n",
        "for i in view_table:\n",
        "  print(i)"
      ],
      "metadata": {
        "id": "uCQ25PXWUIaq"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}