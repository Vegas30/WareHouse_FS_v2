PGDMP      "                }            warehouse_db    17.3    17.3 ,               0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false                       1262    24811    warehouse_db    DATABASE     r   CREATE DATABASE warehouse_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'ru-RU';
    DROP DATABASE warehouse_db;
                     postgres    false            �            1259    24898    order_items    TABLE     J  CREATE TABLE public.order_items (
    order_id integer,
    product_id integer,
    quantity integer NOT NULL,
    unit_price numeric NOT NULL,
    total_price numeric NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    order_item_id integer NOT NULL,
    CONSTRAINT order_items_quantity_check CHECK ((quantity > 0)),
    CONSTRAINT order_items_total_price_check CHECK ((total_price > (0)::numeric)),
    CONSTRAINT order_items_unit_price_check CHECK ((unit_price > (0)::numeric))
);
    DROP TABLE public.order_items;
       public         heap r       postgres    false            �            1259    25051 !   order_items_order_item_id_new_seq    SEQUENCE     �   CREATE SEQUENCE public.order_items_order_item_id_new_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 8   DROP SEQUENCE public.order_items_order_item_id_new_seq;
       public               postgres    false    222                       0    0 !   order_items_order_item_id_new_seq    SEQUENCE OWNED BY     c   ALTER SEQUENCE public.order_items_order_item_id_new_seq OWNED BY public.order_items.order_item_id;
          public               postgres    false    226            �            1259    25048    orders_order_id_seq    SEQUENCE     �   CREATE SEQUENCE public.orders_order_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;
 *   DROP SEQUENCE public.orders_order_id_seq;
       public               postgres    false            �            1259    24882    orders    TABLE     S  CREATE TABLE public.orders (
    order_id integer DEFAULT nextval('public.orders_order_id_seq'::regclass) NOT NULL,
    order_date date NOT NULL,
    supplier_id integer,
    total_amount numeric NOT NULL,
    status text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT orders_status_check CHECK ((status = ANY (ARRAY['в обработке'::text, 'доставлен'::text, 'отменен'::text]))),
    CONSTRAINT orders_total_amount_check CHECK ((total_amount > (0)::numeric))
);
    DROP TABLE public.orders;
       public         heap r       postgres    false    225            �            1259    24832    products    TABLE       CREATE TABLE public.products (
    product_id integer NOT NULL,
    product_name text NOT NULL,
    product_description text,
    category text,
    unit_price numeric NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT products_category_check CHECK ((category = ANY (ARRAY['электроника'::text, 'одежда'::text, 'обувь'::text, 'мебель'::text, 'товары для спорта'::text, 'инструменты'::text, 'бытовая техника'::text, 'здоровье'::text, 'товары для дома'::text, 'продукты'::text]))),
    CONSTRAINT products_unit_price_check CHECK ((unit_price > (0)::numeric))
);
    DROP TABLE public.products;
       public         heap r       postgres    false            �            1259    24864    stock    TABLE     p  CREATE TABLE public.stock (
    stock_id integer NOT NULL,
    product_id integer,
    warehouse_id integer,
    quantity integer NOT NULL,
    last_restocked date,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT stock_quantity_check CHECK ((quantity >= 0))
);
    DROP TABLE public.stock;
       public         heap r       postgres    false            �            1259    24853 	   suppliers    TABLE     L  CREATE TABLE public.suppliers (
    supplier_id integer NOT NULL,
    supplier_name text NOT NULL,
    contact_person text,
    phone_number text,
    email text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT suppliers_email_check CHECK ((email ~ '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'::text)),
    CONSTRAINT suppliers_phone_number_check CHECK ((phone_number ~ '^\d{11}$'::text)),
    CONSTRAINT suppliers_phone_number_not_null CHECK ((phone_number IS NOT NULL))
);
    DROP TABLE public.suppliers;
       public         heap r       postgres    false            �            1259    25030    users    TABLE     `  CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(50) NOT NULL,
    password_hash character varying(255) NOT NULL,
    full_name character varying(100) NOT NULL,
    is_admin boolean DEFAULT false,
    email character varying(100) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.users;
       public         heap r       postgres    false            �            1259    25029    users_user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.users_user_id_seq;
       public               postgres    false    224                       0    0    users_user_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;
          public               postgres    false    223            �            1259    24843 
   warehouses    TABLE     p  CREATE TABLE public.warehouses (
    warehouse_id integer NOT NULL,
    warehouse_name text NOT NULL,
    location text NOT NULL,
    capacity integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT warehouses_capacity_check CHECK ((capacity > 0))
);
    DROP TABLE public.warehouses;
       public         heap r       postgres    false            H           2604    25052    order_items order_item_id    DEFAULT     �   ALTER TABLE ONLY public.order_items ALTER COLUMN order_item_id SET DEFAULT nextval('public.order_items_order_item_id_new_seq'::regclass);
 H   ALTER TABLE public.order_items ALTER COLUMN order_item_id DROP DEFAULT;
       public               postgres    false    226    222            I           2604    25033    users user_id    DEFAULT     n   ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);
 <   ALTER TABLE public.users ALTER COLUMN user_id DROP DEFAULT;
       public               postgres    false    224    223    224                      0    24898    order_items 
   TABLE DATA           �   COPY public.order_items (order_id, product_id, quantity, unit_price, total_price, created_at, updated_at, order_item_id) FROM stdin;
    public               postgres    false    222   J>                 0    24882    orders 
   TABLE DATA           q   COPY public.orders (order_id, order_date, supplier_id, total_amount, status, created_at, updated_at) FROM stdin;
    public               postgres    false    221   �C                 0    24832    products 
   TABLE DATA              COPY public.products (product_id, product_name, product_description, category, unit_price, created_at, updated_at) FROM stdin;
    public               postgres    false    217   hF                 0    24864    stock 
   TABLE DATA           u   COPY public.stock (stock_id, product_id, warehouse_id, quantity, last_restocked, created_at, updated_at) FROM stdin;
    public               postgres    false    220   �T                 0    24853 	   suppliers 
   TABLE DATA           |   COPY public.suppliers (supplier_id, supplier_name, contact_person, phone_number, email, created_at, updated_at) FROM stdin;
    public               postgres    false    219   �`       	          0    25030    users 
   TABLE DATA           i   COPY public.users (user_id, username, password_hash, full_name, is_admin, email, created_at) FROM stdin;
    public               postgres    false    224   !h                 0    24843 
   warehouses 
   TABLE DATA           n   COPY public.warehouses (warehouse_id, warehouse_name, location, capacity, created_at, updated_at) FROM stdin;
    public               postgres    false    218   �h                  0    0 !   order_items_order_item_id_new_seq    SEQUENCE SET     Q   SELECT pg_catalog.setval('public.order_items_order_item_id_new_seq', 153, true);
          public               postgres    false    226                       0    0    orders_order_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.orders_order_id_seq', 55, true);
          public               postgres    false    225                       0    0    users_user_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.users_user_id_seq', 2, true);
          public               postgres    false    223            e           2606    25060    order_items order_items_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (order_item_id);
 F   ALTER TABLE ONLY public.order_items DROP CONSTRAINT order_items_pkey;
       public                 postgres    false    222            c           2606    24892    orders orders_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (order_id);
 <   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_pkey;
       public                 postgres    false    221            Y           2606    24842    products products_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (product_id);
 @   ALTER TABLE ONLY public.products DROP CONSTRAINT products_pkey;
       public                 postgres    false    217            a           2606    24871    stock stock_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.stock
    ADD CONSTRAINT stock_pkey PRIMARY KEY (stock_id);
 :   ALTER TABLE ONLY public.stock DROP CONSTRAINT stock_pkey;
       public                 postgres    false    220            ]           2606    24863    suppliers suppliers_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY public.suppliers
    ADD CONSTRAINT suppliers_pkey PRIMARY KEY (supplier_id);
 B   ALTER TABLE ONLY public.suppliers DROP CONSTRAINT suppliers_pkey;
       public                 postgres    false    219            g           2606    25043    users users_email_key 
   CONSTRAINT     Q   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);
 ?   ALTER TABLE ONLY public.users DROP CONSTRAINT users_email_key;
       public                 postgres    false    224            i           2606    25039    users users_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public                 postgres    false    224            k           2606    25041    users users_username_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);
 B   ALTER TABLE ONLY public.users DROP CONSTRAINT users_username_key;
       public                 postgres    false    224            [           2606    24852    warehouses warehouses_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.warehouses
    ADD CONSTRAINT warehouses_pkey PRIMARY KEY (warehouse_id);
 D   ALTER TABLE ONLY public.warehouses DROP CONSTRAINT warehouses_pkey;
       public                 postgres    false    218            ^           1259    25011    idx_stock_product_id    INDEX     L   CREATE INDEX idx_stock_product_id ON public.stock USING btree (product_id);
 (   DROP INDEX public.idx_stock_product_id;
       public                 postgres    false    220            _           1259    25012    idx_stock_warehouse_id    INDEX     P   CREATE INDEX idx_stock_warehouse_id ON public.stock USING btree (warehouse_id);
 *   DROP INDEX public.idx_stock_warehouse_id;
       public                 postgres    false    220            o           2606    24910 %   order_items order_items_order_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(order_id) ON DELETE CASCADE;
 O   ALTER TABLE ONLY public.order_items DROP CONSTRAINT order_items_order_id_fkey;
       public               postgres    false    4707    221    222            p           2606    24915 '   order_items order_items_product_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(product_id) ON DELETE CASCADE;
 Q   ALTER TABLE ONLY public.order_items DROP CONSTRAINT order_items_product_id_fkey;
       public               postgres    false    4697    217    222            n           2606    24893    orders orders_supplier_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_supplier_id_fkey FOREIGN KEY (supplier_id) REFERENCES public.suppliers(supplier_id) ON DELETE CASCADE;
 H   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_supplier_id_fkey;
       public               postgres    false    221    219    4701            l           2606    24872    stock stock_product_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.stock
    ADD CONSTRAINT stock_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(product_id) ON DELETE CASCADE;
 E   ALTER TABLE ONLY public.stock DROP CONSTRAINT stock_product_id_fkey;
       public               postgres    false    220    217    4697            m           2606    24877    stock stock_warehouse_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.stock
    ADD CONSTRAINT stock_warehouse_id_fkey FOREIGN KEY (warehouse_id) REFERENCES public.warehouses(warehouse_id) ON DELETE CASCADE;
 G   ALTER TABLE ONLY public.stock DROP CONSTRAINT stock_warehouse_id_fkey;
       public               postgres    false    218    220    4699               -  x��ZK�#;\�S��C !�>˻�9�.۫Y�қr��	U�$��:�i�x��W]�����/�^�*��_s1���'V&��|�|��%kX����U2���*�s�m�A~���+Noq��R�6�ʌ;c�������������.�x�������򻀃��� O ������F��9[\�"��l�o���r�틈�4�h���}��M��xnփ�ח�<�S����z�8��i��"����w'k�o����^$��b�XQ��R/kЫ&jz�d��"�ӄ��	��~%�=<�G[~�&�es�%���\�H�\D\Ğ��Cݕ�ur���H����ͣ<�G-2t?���D6b�g[�$G:yO֜4���܄d��ݦ��d�EȻ�8&ߍf]��[������G9^$\&IM*/^�w	%�M{ ��v.�.��-� Y�G휛G�IV��ٱW��dt9$9�n �`K1r�<������炇F'����#=L>^p�59�?�q��1(������q���C����򆃇Ҙ1��&/
h,c �1Ǧ�bm<!�9ơ�'�ϔz��;�0'&A'��9�ݍ�N�z|��,>��L��,��tRhF4�k&�;�AS�7�9i����ϐ7��;�fAԠ>9�|�!}n�+�Ay/zqț?4w���͸k*�Ӵq�e$x�!��!��� ��k\�5����v(;�˧����!��4���������z�;�g\�(�ӮT
|i��J���+��9��Y)l�+�A��J�` �WjZVJ���L�� {�.� I�;��-�
ߩ����.���w�V��;�_wpD�S,��˝b#_n��
9���
��vR,�{���X���b� ���R�*C'���\�N
�E8�
�r�I�`#!�:� ���	l Qi��0�6K�`+��:#�6+�����
� ��R(�ǉå�P��뉥P0��f����P���6�,��pM��Hn�C+��{�kٍ{�P1�{�)�qO� ��rOgr����� $��Խ9���\�]H��� �t.��@. �� �T���T6o�@�+��>P0�z�/���j��hyR^�2�ދh���h�������rl�t�?�,�RFPE�]y΀b)����	�lm��;X�ue<@
q\��H�{��,��^H�+��@
)\�(<SR�L��=P���e>��e>����r(ӕ�`"_�s��.���o��,bH�+�F�N�L^I@��[{��o^�lݸ%X;��ED�/(�         �  x��X�m1��V�n!R�kkI1�+���'נ�(Õ��a��8��G�=�͇EG.H���޻���޿�����~���G���$����#��zOL�m<�Fޱ�ZK��������W@<��l/�	�n�]p��*dZ��E'Ny��D�o�[3�G�8����( %k��%6�@i�;_bst�s��%6zAՖ2��^B��dd/�$�����Q�9MD��hY�ʥ�Q�8���̶T-�"�䰤j�[K���]O�������]5ݭ]��(�����ɽ��U����tū-U��1Ln~������G3�x]��^��ir��O�G�TM�+L��aW�4�R5m��&?��67 /S-�6�7�M�Z�峌*�TM���ar6�j��'��R���?��0L� �)��]��ar���� G���5'[��CzW�9U�0L�]�Z9�s��ͨZ�,0J���^&,�׾��.<���x���'s�eۈF�t4ɲF#?�����,�-0�c�m"a��;w���V�y�h��|J	m�_��ӸI.u�e�#�,��0���͝�_hd
�0C�d״����K��� �Q��bR߮��Q���X�e�;}iB�һU�J�:|�S�{�uT�������iP�:�>p�>����;�P}~�h��:H��� ��D>�vID��k	(tOEh��o��`�ʧ         m  x��[Ys��~ŝ<��$� �Q�b{bIQ^&�XFm�(2�b�o�9cǪ�<�i�$�C;��@$aQ�4���/����s/H�$*д�D���p?��;�T���3v�}��=p��X�Wb���j˵ڶ����Iv��4+�F�n��.�_:�v�댝��s��%�Z�PH˲�ʪ��3)Uc�����l��甜v���&9�u:�Ķc��
w����}�>�/JM�Y�U�.9'��N�m;������(|�B,|:J�I�O�R���=��RdY~�
�y"����m���Q��x����'��.�ς�9r_;g�c��ǀ��b�Fm�ς����{t��)/�����:{\{O˕����]���t(4=F�]�`��`�@��kxO��O�}9��3���|O������z�h<l�լ��[��ٔ����!����Ul0�݃��Y�!���Ȓ��$�y��ħ�LIz�N �t,v�E�V���)��N�	��Z<ST��g�����4eT$@4"#=��P8}�،\���n�/���"����%�	%�Wd:�{K*�I���!|��}N�s1�|L왠�{��">A����pe����QI-KY�a�����~�Got&�-!��xm[��!���,x�7]�K$f�̀��M	��c��%��x�>�*#W;A��ap�x�� �G�S(�û)���/.�L�0	�吸�"��f�EkjH�x{T=�����:&�*@��c䣓�R����X�I�+��:�Ss�J2cAgX>���|M>!��1�1Ix@�$���!Q�1:P�)`��c��x����[��ҽ`t��P-�i�ޡ8|���W��Qӊ��c�7fi��@_�Hѥ��!^}�5L�?�6�´�}�"���!V(���꺯�0�O�y�e@�~�b�J,�*���l��S:�d�4Z�'L�H�uH+K;F��6�Gf��R���-�]A��yo�;�d���yT6@���&��C2��	9��|d�%��V5=�)\J�*�k�2���Q���6�hL6 x	w��<=��><�������������]^R��g ��Ov@> �����[����_�����W�j�I�8����8H��n<5�f�g}}��3��\#�Ȕg���;$A*%6k;l�(Wj�HU�h:�@9{3̗xZ��7�ʡdz��pR�-��U6���tE�M�Z?Pr `�$��!nU�G:�}�-�kͦ��`�ͪ�4�&tfB�/).�BЂ����eb� ��$�L��#�dN(���CF:��z������5�$:� (��#-&��jEe�M@����Q��2ܥ��� f�s/��[gȖ���Y_�fa�u�/1�df�R����M�gk����F��f�4)C�tr���c�C�]�g3�	OSF4C���7n������"ի���0&��\��f�^S���Jͺ�U��X�o�xJ�0ۺ�H��%�Y�&[�[��d�U�<�#m�S��zܽ�ʮ���3��P|���븡�@8��k�M��m,� ��6����4�0��9#�6#��5�Ӏr�F�![n���F�f�.Q��0Pw�I�"��/>k�����:����Ɋ�:[5>�	�����څ9ʓ5y)�K+9�g.����������(m)�*F�1O����erj�+/|j�?U3���\�����`�v�U��p��,�p�X��`^���ZY�ݬ�h���?�~�Cg��!�a�/>.?6�^�Y7�jp
�L���\�>��#����5�����Ɲ�[�s�5���庌17o����Ym4kH��B�l�K&jy��b
'΅!��F�r��:�7:rj�iE@C��� B��|�y�Q��4"�	��4�M�E�`�<C+����Y��צ& f@Ply��[W��cO4����GW�����u�O����d�귏�"fB�+��z�۾HϺ�k�@���i�*O�>��T�v�xn�/�ӳ�F�,���4Z
�%��jKz6�f�BNM�Z�e	O=ħ�Y�0�wE�����3Ϝ��wIF��+����ja� &`�/躜K�0C���֎!ќ�c��\�z��ϛ�C��Y��h/��Y��n��m��Ө4����4�a��j@���+^���t��S��,������б~Hdv|��Sc�ƙ�8g���sb�0oŭ�	�K�q��������ݻ�p����q����E�1ϝ��O̼#<�����h��хW7+�f<+?1��zJ���ʂ�0^S��<����gK�D@�* kdr�DߥD��k1�IN���ޑ�FNɂD�c~�y)�.
8�;��=�<���}����AON�K�Ŕ��N��;���f{|t`� �i-�xA���}�̸yDna�:�h��?�VM�'� T�d�r~w9Έ���qҴ�}bl�����fc*�����Iӝ�]�;���d�IT6}K4���\r3���	�����ҧF�q��$hչ$oT���(T.}����o�G���4�DV��0e��*�^�#b�* �����[��I�:�j>:M�킎h��@�|?k�r�QAjA�9�7���������U2Bq.������TR �
#W���M��!��$z�|FCk
�P?��,e�4�M=?;M�_JTN�#j�c�>v����3�^5hn�~����-S�:��Wؾ���� ����]�jF����,���$<Y]��]A��Cn#QkC7�F��yZ���6`���}�(t�Ŀ0:P��<��>�3����E���dSˣ�v��C��rcalY����E0o?h�f_-W��m�D�m���48E�PTN�0�my�m	�`SuA40r$\y��.���)�E�L��1?���"����a9�FP�Ю=]�B+�0ꐏE~L�k�<c"-���閶<�n"�Sj1��PLl��1[$W���X��v���(X~ӏvL��D�4�ST����e&�~��I��Qo���(�.�#�Ba��5�YPqʧF8�P�2JpH(��Q����.��?-+�})�UqgE0`�#����p���~�h�)�fڠͥ  5L�W �unH'�@m�v|�,�N#o�1�y7�;2��B��+��H^�y�:�b�db�y��I�Ŭ+ ���X$���' nF���ĝ�cʚ�fa���7�����s��T��:]���RW ��[1=�oPL:���p����0ߘ����kSov�"*9��5�w�ǋR����5#��]�+�(`:���(���2�H�3�d"��Jr<����hu�¶	b��q��ӈ�((��ك����7Yf�%*���MgBm�"@ c�<��r�,�� ���?�wjn�X�!��I�!@q������{���{̔z�̘g<o�i!�y�$��4j�6�,�G��P(�}am>���p�Zb�Ȅ��6pы�$){�5�œ\���s�&d�-H�4�^_o>��@��Q�{J����'��8�+=���}��ru��Z1/+/�O�k��W�Ï�"P6ۨ=��k[۬���َ�T��o7.��}щ_إ��͎yn��lը7�jCR���� ���42��0P!3>�-i�+��嵜�'~�N$��$         �  x���m��6DS��V`f����Ȁ�]�+Q�Mu%�rY[�$�Ck�J=�Q�V���?����m�_�?�=ʼ[�:�G7+�h�Gm_��Q�2����V?j����/X�����y~_��h���;���=o��8<��X���2lc샫��?�o��[��Ï߳�]>�<��r����[�ȩ6�{��˳#�W�V^������V;��xh��c��c�s<��hu=�9�o�ڏ�#��~,�/�������������� �냐��ʟ�7���>HΪ��z.���t��w��9�~,��O5Q}�I�\)�ӷ�fp���r}�m~nzy�?���9�G ���[}�fh�X����2-'�^>��F��"��W�����=F��n���y�x�|��kik����(��o�>�_u=j}��s�l��X�����Z+/��׬�߶���U��3ϲ?�{c�j����L/��ߜ�������9��c��ol�>�k�/��ۛ�Tss��sw�?�O�����T��{�П��s_B�Y����X�ϣ)�y�Ο�+�9I�ϣ+�y�?��\s��s�pϥC�ϳI�9�A��ӥ�<C�ϳK�y�?�]*�織Z��V����eR9�1���^rur��P��ط�H��G(G{�Wɑ���#ϙ �#�EV&G^L(G^\&G��L��t�y��N�<��ur�e	��7G%G�L'G�ç�#O�ʑ�^&G��A(G��L���y��N�<OR'G�/�L�<�x�y����g�S�Z�\�Z��R�ky�B��2�������V�Z�K�2ײ*t�4#�k�	]�\�Z:ײ�t-Bײ�t�4�k�8
]�\9T��M�ZnJ�r���>&�ky����k���B��t�<2�kEU�V4�k�I]�%D�ZydJ׊�s�J׊)t�XB��uH�Z��d�՛еr�W�Vw�k����~'�r��]��էе�R����k��B�M�ZÔ�5\�Z9e��5�ҵr�P�֘B�K�ZyLB���E�Z�)]+EK�Zӥ�5C�Z�K]k�V�V��BךKwd{��,7��&��eJ��e�ۻ�W�Z�B\Si��RY`�"���Ug��������c�`�Y`��Y`�.���Hg�����,�F���#'��c��:�jB�D�,0�q�,0�;f��~ɬ���/�e9ׄ��\+�h�\+�6��V�`�\+�ҹV��ȵ�u�kEޠB׊�d�{吹V䴐��U�k�ӹ��ҵ̕��_0�\˺еl(]˦ҵ�t-/J���[�Zބ��&u-w�k����w�k�w�:��o�urE*G������!��!�����!��!��!��!��]��#���Gte���ѕ=<�+{xDW���.��]��#���Gi����hH{xĐ�݈�l�C�v#��Ee7��n1��(bJ�Q�l:=������t��¦ӣٕz4�P�r����\R=�c��Q�	B=ZM�G˔z�K�N�Ҋ�z��R���-N�)ԣ��Ӌ���l/�M�5r;�*���xh�Fn��4_#�s����۹F��ǎ�x�$Mv�\�]�c��|jz����M���w�TI�?p���s�;~.�]�b����V�n��Y+��8yc�g�����z>CQ�]l��'x�����D}lr��
����Ż�O�z&����31���S���L���O���3�u#��g����=W��_����q���{-Z�^�����e����Z��v����*�,��Y�ҳ(T�gY�BϢ@}�E��<�y�kӰוy�
�4��i*��0T��a�(O�@M�f��<Cyze�y����4��i�M�`e����>Cu}���4U�i,��J�j�4��i���B� �A4T�h*�0P�Y�D�P%��XP�Y�D�@�f�*E �j@4��h*��0PN�Y����`i����MC�)�R4��h�J�0T��a�&E�PI���MCec'h���	�B'hȜ�Y r�f��	'hț`Y8n����	���&h��	��&hH��Y(h����	�b&hH�`Y0d����	#&hJ��a0`���|	��%hJ��a(\���l	�%hXUV�`N�14�uJ�
�L��
�"*hJ��a ��eUP��`@�<T��<+�/�P@C<T�4PA�P@C<T�4P��P@O�<T�0P��P@OC4T�4P��P�O��<�u��B�<$J�0�(��P�MC�<$J�0�(��@�C�<�u��B�<$J�0�(��P�M��<$J�0�(��P�O��<.�r�%x��q(����V�>C x��q(����:�g��B x��a0���B x��q �����:�g��B x
��i0����B x
��i(����B x��q ���C x
��i(����C x
��i0�ǽ��YS�Z �f��B x��a(���B x��q �����:�e5��@C!<�@�4��@C!<�@�4��PM�!<�@�0��POC!<-����!<�@�8��`�!<�
]��B x
��i ���C x��a(����U���B x
��i(����B x
��i(�~J���ܫ~�ߟ͐��g>�xĺ�}�<8�)A�+̔�i0S����b x���i(����6��S%hN��q�NU0U��	�U5�*�Ô�J��a®U�J�8a�S%x��wU��<Mؽ��T	���_�`�Ov�j0U��I{X�T	'�b�S%x������q�NV0���I{Y��
�&�f�`DO���j ��g��
�"*x���a(�����
"*x���q(�����
��:��g��
�"*x���i(���)�[�"*x��Õ�
��2?�"d��#?��R�����u/����G�G�w���U�����o�)l         ;  x��X]S�F}^~���x�,Y2O䋦S2��}�b��Y�d7�����)�0e���/�p�` a��z���!�0��JG�{���ɬ.��0��x���N����`u�_�#�!���a�f�DjrA3`3ˎ_�O
A��S�99U�ԋ9͚6�i�*��^����h�H���s~����S��x�w��`~���-�����XFٴ,˶�e�ʢ�~d�W�i8��� �U@�?��(x����?�=~�/2hz�0K��
V�xn}��M|ޣ�*�b������d��l��w@Aw��%e�*�F�8��5� 
I(~��=߆�g�C\�U�w�)�هR �=�^_BN$%6	��-/�FӣK��4,�E��A= K=�'Rv? �u�lE��En�]�"Zw"�$r=�ȎMf�>p�%�	\t MWH 9��:��"+��,m���b)��nݍo�� �e��z���K}�6���-� ��*�>k��&[W��.tq�zp�.m�
[į+kA�jJ}��$ĸ�Z%� !�s� tP�X/.%l�����A#���H�.zr�`=��	�e�ڶ�ʕ4����J�(
<�5<�18�J̍T��C�?@�𳗀"�I�O��C�݊j�h��G�Y�J�JU�ms|C(��T6��)�LC\��ԵR"k5x�9קb���:����>����O���q0�΃u�5��-�廁ۦ�М	�:��-^��j������TKa��-��
#,0��K�ʉY��)�u��&�[��q���ɂt��qb�a��#��}�@�[�N������ob��Sd6��"Z�|���\���B�(֫���x[��ή(]#_/�3�A�
A��t��8��t&�����5n"��:z���v��|�Z�6B�[��������+0%	��W�
3uQ�
k|)�"v��_�Kqn�Y��J������C9��ǎ����Hg��T X�_�y'�U����Lrj@V	\���d83A���A.��!��ubCq��f����� �gB@��S�}�Rbz#G��?��@��V%�C�2"6f��dy �a<=��+��ᩝиh.�C6n�j6����
}:��IY� ʣ)�#k�3�7
}�V�U�T�JRV:�gl��Ծ�/�"�8]��܊�>��@�6��:�$v�m�&��0�L��1eP:yP��J�Ġ���;��n�U���X$����a�i 	�vĶMn�C�l����\�~�G��IHYX c�!�"��&y، �f�n(��&(��b�P�#�1liIc��U��"���q���"g�Ԑ�G�0��k�Gm���$BÓ4��`ƿ�r9�G.���}�p�S�Z���Ȕe��R�(�֘�~���AG{�k���Hl7?rd�9��v��N=`u꫞�iW��cˡ~��9�|f���9f(�Ў����$CO!�'~_�t�$�?��-�)�4�Ê��TL��B��1�B�^�7���D�>�5꩞&��}��~�	p���]�6	�� �_0h�#���-4΍X٢n�Ss�(XV��DJ��u s���;RHyY�U�,�7𳉚��[V����D�u��/P�;q�ލI�m7������
�J�ۃjm "����v@H/��B]���|��<<7U>04�q����Mș���E�v��j}�
��t\���Ix�	ta�է�����`�t3'h�T�>���1I�7�͆���B��W�&����d�x��&���v#�����Ƥ��"~T��U���f�;u�;n�|uD���!�TpuV.k�,M��e5{��������j      	   �   x�3�LL��̃��FƜ&\�raυ�^�q��b�ņ.6]�w�A��B�Ѕ��\��,�hr(O,J��/-N�+*�4202�50�54T04�24�22�35�43��2��M�KLO-��`�� M��[.l��dɜ.l��`7l�L�)'ڢ=... �G[�         �  x��Wk��0�mN�d;1���P��J[	�j�UՖ�Vm��<�,,��7�g"Lȣ�d<��7�F����h�g:�X.h�OZ�^�����ہӮ�T�@O�F����U�fz��s�$�*�Q(�@�O*��^��I�V+r }�8�#Z���ziɊ62t�X�W�Y_y�\_p�%eCs��1î�k0����)�'<���o���г�9�c;����~ױg�π��0����z̊���&8���-q��f��=̮ !�s���+��7�-�D=��F��U&������;����{�큹�j�]�p����dȧ;_Ԁ��j C:0���P����V�_8�NOL���,����G�T��~e|a�7�A]F$�%>����byU5�Eh�=9U�+�R� �En��[�u�����-�7n��c���Y.�(a9Uy5h�[˾�������2F�ӁKӁ`Njr�(TdM��^���e"���u2��B溎����;K߫�d��c�.ʉ`z�5[v]]+wdnu����^qh��LΩ�S��EUw�!�b�9�aAS[�%q� ���s�o����D��%�%�hU�47 ҃���Ux�.�I�y�Hӭ�������ՙ�B��e��14��7�~�dB�Nu�!%�E�w��^<�״a'�:��F���I�1���S.���M���2_I���晗��-�u�š���Q2�e'ݾ�[/:�V�����     